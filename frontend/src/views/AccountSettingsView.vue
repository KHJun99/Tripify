<template>
  <div class="mypage-container">
    <div class="mypage-card">
      <h2 class="page-title">마이페이지</h2>

      <!-- 회원 정보 섹션 -->
      <section class="info-section">
        <h3 class="section-title">회원 정보</h3>
        <div class="info-grid" v-if="user">
          <div class="info-item">
            <label>아이디</label>
            <span>{{ user.username }}</span>
          </div>
          <div class="info-item">
            <label>이메일</label>
            <span>{{ user.email }}</span>
          </div>
          <div class="info-item">
            <label>로그인 타입</label>
            <span>{{ getLoginTypeLabel(user.login_type) }}</span>
          </div>
          <div class="info-item">
            <label>가입일</label>
            <span>{{ formatDate(user.created_at) }}</span>
          </div>
          <div class="info-item" v-if="user.preferred_region">
            <label>선호 지역</label>
            <span>{{ user.preferred_region }}</span>
          </div>
          <div class="info-item" v-if="user.travel_style">
            <label>여행 스타일</label>
            <span>{{ user.travel_style }}</span>
          </div>
        </div>
      </section>

      <hr class="divider" />

      <!-- 비밀번호 변경 섹션 (일반 로그인만) -->
      <section class="password-section" v-if="isNormalLogin">
        <h3 class="section-title">비밀번호 변경</h3>

        <form @submit.prevent="handlePasswordChange" class="password-form">
          <div class="form-group">
            <label for="current-password">현재 비밀번호</label>
            <input
              type="password"
              id="current-password"
              v-model="passwordForm.currentPassword"
              placeholder="현재 비밀번호를 입력하세요"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="new-password">새 비밀번호</label>
            <input
              type="password"
              id="new-password"
              v-model="passwordForm.newPassword"
              placeholder="새 비밀번호를 입력하세요"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="new-password-confirm">새 비밀번호 확인</label>
            <input
              type="password"
              id="new-password-confirm"
              v-model="passwordForm.newPasswordConfirm"
              placeholder="새 비밀번호를 다시 입력하세요"
              class="form-input"
            />
          </div>

          <div v-if="passwordError" class="error-message">
            {{ passwordError }}
          </div>

          <div v-if="passwordSuccess" class="success-message">
            {{ passwordSuccess }}
          </div>

          <button
            type="submit"
            class="change-password-button"
            :disabled="isChangingPassword || !isPasswordFormValid"
          >
            {{ isChangingPassword ? '변경 중...' : '비밀번호 변경' }}
          </button>
        </form>
      </section>

      <section class="password-section" v-else>
        <h3 class="section-title">비밀번호 변경</h3>
        <p class="info-text">소셜 로그인 사용자는 비밀번호를 변경할 수 없습니다.</p>
      </section>

      <hr class="divider" />

      <!-- 회원탈퇴 섹션 -->
      <section class="delete-section">
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
      </section>
    </div>

    <!-- 회원탈퇴 확인 모달 -->
    <div v-if="showDeleteConfirmation" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal-content">
        <h3 class="modal-title">회원탈퇴 확인</h3>
        <p class="modal-warning">
          정말로 회원탈퇴를 하시겠습니까?<br />
          모든 데이터가 삭제되며 복구할 수 없습니다.
        </p>

        <!-- 일반 로그인 사용자는 비밀번호 입력 필요 -->
        <div v-if="isNormalLogin" class="password-input-section">
          <label for="delete-password">비밀번호 확인</label>
          <input
            type="password"
            id="delete-password"
            v-model="deletePassword"
            placeholder="비밀번호를 입력하세요"
            class="password-input"
            @keyup.enter="handleDeleteAccount"
          />
        </div>

        <div v-if="deleteError" class="error-message">
          {{ deleteError }}
        </div>

        <div class="modal-buttons">
          <button
            @click="handleDeleteAccount"
            class="confirm-button"
            :disabled="isDeleting || (isNormalLogin && !deletePassword)"
          >
            {{ isDeleting ? '처리 중...' : '탈퇴하기' }}
          </button>
          <button
            @click="closeDeleteModal"
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
const deletePassword = ref('')
const isDeleting = ref(false)
const deleteError = ref('')

// 비밀번호 변경 관련
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  newPasswordConfirm: '',
})
const isChangingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

// 일반 로그인 사용자인지 확인
const isNormalLogin = computed(() => {
  return user.value && (!user.value.login_type || user.value.login_type === 'normal')
})

// 비밀번호 폼 유효성 검사
const isPasswordFormValid = computed(() => {
  return (
    passwordForm.value.currentPassword &&
    passwordForm.value.newPassword &&
    passwordForm.value.newPasswordConfirm
  )
})

onMounted(async () => {
  try {
    user.value = await authStore.getProfile()
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    router.push('/login')
  }
})

const getLoginTypeLabel = (type) => {
  const labels = {
    normal: '일반 로그인',
    kakao: '카카오 로그인',
    google: '구글 로그인',
  }
  return labels[type] || '일반 로그인'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const handlePasswordChange = async () => {
  if (isChangingPassword.value) return

  passwordError.value = ''
  passwordSuccess.value = ''

  // 클라이언트 측 유효성 검사
  if (passwordForm.value.newPassword !== passwordForm.value.newPasswordConfirm) {
    passwordError.value = '새 비밀번호가 일치하지 않습니다.'
    return
  }

  if (passwordForm.value.newPassword.length < 8) {
    passwordError.value = '새 비밀번호는 최소 8자 이상이어야 합니다.'
    return
  }

  try {
    isChangingPassword.value = true

    await authStore.changePassword(
      passwordForm.value.currentPassword,
      passwordForm.value.newPassword,
      passwordForm.value.newPasswordConfirm
    )

    passwordSuccess.value = '비밀번호가 성공적으로 변경되었습니다.'

    // 폼 초기화
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      newPasswordConfirm: '',
    }

    // 3초 후 성공 메시지 제거
    setTimeout(() => {
      passwordSuccess.value = ''
    }, 3000)
  } catch (error) {
    console.error('비밀번호 변경 실패:', error)
    if (error.response?.data?.error) {
      passwordError.value = error.response.data.error
    } else if (error.response?.data?.current_password) {
      passwordError.value = error.response.data.current_password[0]
    } else if (error.response?.data?.new_password) {
      passwordError.value = error.response.data.new_password[0]
    } else {
      passwordError.value = '비밀번호 변경 중 오류가 발생했습니다.'
    }
  } finally {
    isChangingPassword.value = false
  }
}

const closeDeleteModal = () => {
  if (!isDeleting.value) {
    showDeleteConfirmation.value = false
    deletePassword.value = ''
    deleteError.value = ''
  }
}

const handleDeleteAccount = async () => {
  if (isDeleting.value) return

  // 일반 로그인 사용자는 비밀번호 확인 필수
  if (isNormalLogin.value && !deletePassword.value) {
    deleteError.value = '비밀번호를 입력해주세요.'
    return
  }

  try {
    isDeleting.value = true
    deleteError.value = ''

    const passwordToSend = isNormalLogin.value ? deletePassword.value : null
    await authStore.deleteAccount(passwordToSend)

    alert('회원탈퇴가 완료되었습니다.')
    router.push('/')
  } catch (error) {
    console.error('회원탈퇴 실패:', error)
    if (error.response?.data?.error) {
      deleteError.value = error.response.data.error
    } else {
      deleteError.value = '회원탈퇴 처리 중 오류가 발생했습니다.'
    }
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.mypage-container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.mypage-card {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #222;
  font-weight: 700;
}

.section-title {
  font-size: 1.4rem;
  margin-bottom: 1.25rem;
  color: #333;
  font-weight: 600;
}

.info-section {
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.info-item label {
  font-weight: 600;
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  color: #212529;
  font-size: 1rem;
  font-weight: 500;
}

.divider {
  border: none;
  border-top: 2px solid #e9ecef;
  margin: 2.5rem 0;
}

.password-section {
  margin-bottom: 2rem;
}

.info-text {
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.6;
}

.password-form {
  max-width: 500px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.change-password-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.change-password-button:hover:not(:disabled) {
  background-color: #45a049;
}

.change-password-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.delete-section {
  margin-top: 2rem;
}

.danger-title {
  font-size: 1.4rem;
  color: #dc3545;
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.warning-text {
  color: #6c757d;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
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

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 0.875rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  border: 1px solid #f5c6cb;
}

.success-message {
  background-color: #d4edda;
  color: #155724;
  padding: 0.875rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  border: 1px solid #c3e6cb;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 700;
}

.modal-warning {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.password-input-section {
  margin-bottom: 1.5rem;
}

.password-input-section label {
  display: block;
  margin-bottom: 0.5rem;
  color: #495057;
  font-weight: 600;
}

.password-input {
  width: 100%;
  padding: 0.875rem;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.password-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.modal-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.confirm-button,
.cancel-button {
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
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

@media (max-width: 768px) {
  .mypage-card {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .modal-buttons {
    flex-direction: column-reverse;
  }

  .confirm-button,
  .cancel-button {
    width: 100%;
  }
}
</style>
