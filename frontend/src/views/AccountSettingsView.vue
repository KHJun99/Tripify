<template>
  <div class="account-settings-container">
    <div class="settings-card">
      <h2 class="settings-title">계정 설정</h2>

      <!-- 회원 정보 -->
      <div class="user-info-section">
        <h3>회원 정보</h3>
        <div class="info-item" v-if="user">
          <label>아이디:</label>
          <span>{{ user.username }}</span>
        </div>
        <div class="info-item" v-if="user">
          <label>이메일:</label>
          <span>{{ user.email }}</span>
        </div>
      </div>

      <hr class="divider" />

      <!-- 회원탈퇴 섹션 -->
      <div class="delete-account-section">
        <h3 class="danger-title">회원탈퇴</h3>
        <p class="warning-text">
          회원탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.
        </p>

        <button
          @click="showDeleteConfirmation = true"
          class="delete-button"
          :disabled="isDeleting"
        >
          회원탈퇴
        </button>
      </div>
    </div>

    <!-- 회원탈퇴 확인 모달 -->
    <div v-if="showDeleteConfirmation" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3 class="modal-title">회원탈퇴 확인</h3>
        <p class="modal-warning">
          정말로 회원탈퇴를 하시겠습니까?<br />
          모든 데이터가 삭제되며 복구할 수 없습니다.
        </p>

        <!-- 일반 로그인 사용자는 비밀번호 입력 필요 -->
        <div v-if="requiresPassword" class="password-input-section">
          <label for="password">비밀번호 확인</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="비밀번호를 입력하세요"
            class="password-input"
            @keyup.enter="handleDeleteAccount"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="modal-buttons">
          <button
            @click="handleDeleteAccount"
            class="confirm-button"
            :disabled="isDeleting || (requiresPassword && !password)"
          >
            {{ isDeleting ? '처리 중...' : '탈퇴하기' }}
          </button>
          <button
            @click="closeModal"
            class="cancel-button"
            :disabled="isDeleting"
          >
            취소
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = ref(null)
const showDeleteConfirmation = ref(false)
const password = ref('')
const isDeleting = ref(false)
const errorMessage = ref('')

// 일반 로그인 사용자는 비밀번호 확인 필요
const requiresPassword = computed(() => {
  return user.value && (!user.value.loginType || user.value.loginType === 'normal')
})

onMounted(async () => {
  try {
    user.value = await authStore.getProfile()
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    router.push('/login')
  }
})

const closeModal = () => {
  if (!isDeleting.value) {
    showDeleteConfirmation.value = false
    password.value = ''
    errorMessage.value = ''
  }
}

const handleDeleteAccount = async () => {
  if (isDeleting.value) return

  // 일반 로그인 사용자는 비밀번호 확인 필수
  if (requiresPassword.value && !password.value) {
    errorMessage.value = '비밀번호를 입력해주세요.'
    return
  }

  try {
    isDeleting.value = true
    errorMessage.value = ''

    const passwordToSend = requiresPassword.value ? password.value : null
    await authStore.deleteAccount(passwordToSend)

    alert('회원탈퇴가 완료되었습니다.')
    router.push('/')
  } catch (error) {
    console.error('회원탈퇴 실패:', error)
    if (error.response?.data?.error) {
      errorMessage.value = error.response.data.error
    } else {
      errorMessage.value = '회원탈퇴 처리 중 오류가 발생했습니다.'
    }
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.account-settings-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.settings-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.settings-title {
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.user-info-section {
  margin-bottom: 2rem;
}

.user-info-section h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #555;
}

.info-item {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item label {
  font-weight: 600;
  width: 120px;
  color: #666;
}

.info-item span {
  color: #333;
}

.divider {
  border: none;
  border-top: 2px solid #f0f0f0;
  margin: 2rem 0;
}

.delete-account-section {
  margin-top: 2rem;
}

.danger-title {
  font-size: 1.25rem;
  color: #dc3545;
  margin-bottom: 0.75rem;
}

.warning-text {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.delete-button:hover:not(:disabled) {
  background-color: #c82333;
}

.delete-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.modal-warning {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.password-input-section {
  margin-bottom: 1.5rem;
}

.password-input-section label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 600;
}

.password-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.password-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.confirm-button,
.cancel-button {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.confirm-button {
  background-color: #dc3545;
  color: white;
}

.confirm-button:hover:not(:disabled) {
  background-color: #c82333;
}

.confirm-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
}

.cancel-button:hover:not(:disabled) {
  background-color: #5a6268;
}

.cancel-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
