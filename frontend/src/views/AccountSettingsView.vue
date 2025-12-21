<template>
  <div class="mypage-container">
    <!-- 비밀번호 확인 모달 (일반 로그인 사용자만) -->
    <div v-if="showPasswordVerification" class="modal-overlay">
      <div class="modal-content verification-modal">
        <h3 class="modal-title">마이페이지 접근 인증</h3>
        <p class="modal-info">
          보안을 위해 비밀번호를 입력해주세요.
        </p>

        <div class="password-input-section">
          <label for="verify-password">비밀번호</label>
          <input
            type="password"
            id="verify-password"
            v-model="verifyPassword"
            placeholder="비밀번호를 입력하세요"
            class="password-input"
            @keyup.enter="handlePasswordVerification"
            autofocus
          />
        </div>

        <div v-if="verifyError" class="error-message">
          {{ verifyError }}
        </div>

        <div class="modal-buttons">
          <button
            @click="handlePasswordVerification"
            class="verify-button"
            :disabled="isVerifying || !verifyPassword"
          >
            {{ isVerifying ? '확인 중...' : '확인' }}
          </button>
          <button
            @click="handleCancelVerification"
            class="cancel-button"
            :disabled="isVerifying"
          >
            취소
          </button>
        </div>
      </div>
    </div>

    <!-- 마이페이지 컨텐츠 -->
    <div v-if="isVerified" class="mypage-content">
      <div class="mypage-card">
        <div class="page-header">
          <h2 class="page-title">👤 마이페이지</h2>
          <p class="page-subtitle">계정 정보 및 설정을 관리하세요</p>
        </div>

        <!-- 회원 정보 섹션 -->
        <section class="info-section">
          <h3 class="section-title">
            <span class="section-icon">📋</span>
            회원 정보
          </h3>
          <div class="info-grid" v-if="user">
            <div class="info-item">
              <div class="info-icon">👤</div>
              <div class="info-content">
                <label>아이디</label>
                <span>{{ user.username }}</span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon">📧</div>
              <div class="info-content">
                <label>이메일</label>
                <span>{{ user.email }}</span>
              </div>
            </div>
            <div class="info-item editable">
              <div class="info-icon">✨</div>
              <div class="info-content">
                <label>닉네임</label>
                <div v-if="!isEditingNickname" class="nickname-display">
                  <span>{{ user.nickname || '닉네임이 없습니다' }}</span>
                  <button @click.stop="startEditNickname" class="edit-btn">✏️ 수정</button>
                </div>
                <div v-else class="nickname-edit">
                  <input 
                    v-model="editingNickname" 
                    type="text" 
                    class="nickname-input"
                    placeholder="닉네임을 입력하세요"
                    maxlength="50"
                    @keyup.enter="saveNickname"
                    @keyup.esc="cancelEditNickname"
                    ref="nicknameInputRef"
                  />
                  <div class="edit-buttons">
                    <button @click.stop="saveNickname" class="save-btn" :disabled="isSavingNickname">저장</button>
                    <button @click.stop="cancelEditNickname" class="cancel-btn">취소</button>
                  </div>
                </div>
                <div v-if="nicknameError" class="nickname-error">{{ nicknameError }}</div>
                <div v-if="nicknameSuccess" class="nickname-success">{{ nicknameSuccess }}</div>
              </div>
            </div>
            <div class="info-item highlight">
              <div class="info-icon">🔐</div>
              <div class="info-content">
                <label>로그인 타입</label>
                <span class="login-type-badge" :class="getLoginTypeClass(user.login_type)">
                  {{ getLoginTypeLabel(user.login_type) }}
                </span>
              </div>
            </div>
            <div class="info-item">
              <div class="info-icon">📅</div>
              <div class="info-content">
                <label>가입일</label>
                <span>{{ formatDate(user.created_at) }}</span>
              </div>
            </div>
            <div class="info-item" v-if="user.preferred_region">
              <div class="info-icon">📍</div>
              <div class="info-content">
                <label>선호 지역</label>
                <span>{{ user.preferred_region }}</span>
              </div>
            </div>
            <div class="info-item" v-if="user.travel_style">
              <div class="info-icon">🎨</div>
              <div class="info-content">
                <label>여행 스타일</label>
                <span>{{ user.travel_style }}</span>
              </div>
            </div>
          </div>
        </section>

        <div class="divider"></div>

        <!-- 비밀번호 변경 섹션 (일반 로그인만) -->
        <section class="password-section" v-if="isNormalLogin">
          <h3 class="section-title">
            <span class="section-icon">🔑</span>
            비밀번호 변경
          </h3>

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
          <h3 class="section-title">
            <span class="section-icon">🔑</span>
            비밀번호 변경
          </h3>
          <div class="info-box">
            <p class="info-text">
              <span class="info-icon-text">ℹ️</span>
              소셜 로그인 사용자는 비밀번호를 변경할 수 없습니다.
            </p>
          </div>
        </section>

        <div class="divider"></div>

        <!-- 회원탈퇴 섹션 -->
        <section class="delete-section">
          <h3 class="danger-title">
            <span class="section-icon">⚠️</span>
            회원탈퇴
          </h3>
          <div class="warning-box">
            <p class="warning-text">
              회원탈퇴 시 모든 데이터가 삭제되며 복구할 수 없습니다.
            </p>
          </div>

          <button
            @click="showDeleteConfirmation = true"
            class="delete-button"
            :disabled="isDeleting"
          >
            <span>🗑️</span>
            회원탈퇴
          </button>
        </section>
      </div>
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
import { authAPI } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = ref(null)
const showDeleteConfirmation = ref(false)
const deletePassword = ref('')
const isDeleting = ref(false)
const deleteError = ref('')

// 비밀번호 확인 관련
const showPasswordVerification = ref(false)
const verifyPassword = ref('')
const isVerifying = ref(false)
const verifyError = ref('')
const isVerified = ref(false)

// 비밀번호 변경 관련
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  newPasswordConfirm: '',
})
const isChangingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

// 닉네임 수정 관련
const isEditingNickname = ref(false)
const editingNickname = ref('')
const isSavingNickname = ref(false)
const nicknameError = ref('')
const nicknameSuccess = ref('')
const nicknameInputRef = ref(null)

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

    // 일반 로그인 사용자는 비밀번호 확인 필요
    if (isNormalLogin.value) {
      showPasswordVerification.value = true
    } else {
      // 소셜 로그인 사용자는 바로 접근
      isVerified.value = true
    }
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    router.push('/login')
  }
})

const startEditNickname = () => {
  editingNickname.value = user.value?.nickname || ''
  isEditingNickname.value = true
  nicknameError.value = ''
  nicknameSuccess.value = ''
  // 다음 틱에서 포커스
  setTimeout(() => {
    if (nicknameInputRef.value) {
      nicknameInputRef.value.focus()
    }
  }, 0)
}

const cancelEditNickname = () => {
  isEditingNickname.value = false
  editingNickname.value = ''
  nicknameError.value = ''
  nicknameSuccess.value = ''
}

const saveNickname = async () => {
  if (isSavingNickname.value) return
  
  nicknameError.value = ''
  nicknameSuccess.value = ''
  
  if (!editingNickname.value.trim()) {
    nicknameError.value = '닉네임을 입력해주세요.'
    return
  }
  
  if (editingNickname.value.trim().length > 50) {
    nicknameError.value = '닉네임은 50자 이하여야 합니다.'
    return
  }
  
  try {
    isSavingNickname.value = true
    const updatedUser = await authStore.updateProfile({ nickname: editingNickname.value.trim() })
    user.value = updatedUser
    nicknameSuccess.value = '닉네임이 변경되었습니다.'
    isEditingNickname.value = false
    
    // 3초 후 성공 메시지 제거
    setTimeout(() => {
      nicknameSuccess.value = ''
    }, 3000)
  } catch (error) {
    console.error('닉네임 변경 실패:', error)
    if (error.response?.data?.nickname) {
      nicknameError.value = error.response.data.nickname[0]
    } else {
      nicknameError.value = '닉네임 변경 중 오류가 발생했습니다.'
    }
  } finally {
    isSavingNickname.value = false
  }
}

const handlePasswordVerification = async () => {
  if (isVerifying.value || !verifyPassword.value) return

  try {
    isVerifying.value = true
    verifyError.value = ''

    await authAPI.verifyPassword(verifyPassword.value)

    // 비밀번호 확인 성공
    showPasswordVerification.value = false
    isVerified.value = true
  } catch (error) {
    console.error('비밀번호 확인 실패:', error)
    if (error.response?.data?.password) {
      verifyError.value = error.response.data.password[0]
    } else {
      verifyError.value = '비밀번호가 올바르지 않습니다.'
    }
  } finally {
    isVerifying.value = false
  }
}

const handleCancelVerification = () => {
  router.push('/')
}

const getLoginTypeLabel = (type) => {
  const labels = {
    normal: '일반 로그인',
    kakao: '카카오 로그인',
    google: '구글 로그인',
  }
  return labels[type] || '일반 로그인'
}

const getLoginTypeClass = (type) => {
  const classes = {
    normal: 'login-normal',
    kakao: 'login-kakao',
    google: 'login-google',
  }
  return classes[type] || 'login-normal'
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
  background: #f5f7fa;
  min-height: 100vh;
  padding: 2rem 1rem;
}

.mypage-content {
  max-width: 900px;
  margin: 0 auto;
}

.mypage-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e8ecef;
}

.page-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 3px solid #3498db;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #1a1a1a;
  font-weight: 700;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  font-weight: 500;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-icon {
  font-size: 1.3rem;
}

.info-section {
  margin-bottom: 2.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e8ecef;
  border-left: 4px solid #3498db;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-item.highlight {
  background: linear-gradient(135deg, #fff5e6 0%, #ffe8cc 100%);
  border-left-color: #ff9800;
}

.info-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  font-size: 0.85rem;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  color: #1a1a1a;
  font-size: 1.1rem;
  font-weight: 600;
}

.login-type-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.login-type-badge.login-normal {
  background: #e3f2fd;
  color: #1976d2;
}

.login-type-badge.login-kakao {
  background: #fef3e2;
  color: #f9a825;
}

.login-type-badge.login-google {
  background: #e8f5e9;
  color: #388e3c;
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #e8ecef, transparent);
  margin: 2.5rem 0;
  border: none;
}

.password-section {
  margin-bottom: 2.5rem;
}

.info-box {
  padding: 1.25rem;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 4px solid #3498db;
}

.info-text {
  color: #495057;
  font-size: 1rem;
  line-height: 1.6;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-icon-text {
  font-size: 1.2rem;
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
  padding: 0.875rem 1rem;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.change-password-button {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.change-password-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.change-password-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.delete-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #fff5f5;
  border-radius: 12px;
  border: 2px solid #ffebee;
}

.danger-title {
  font-size: 1.5rem;
  color: #dc3545;
  margin-bottom: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.warning-box {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #dc3545;
}

.warning-text {
  color: #495057;
  margin: 0;
  line-height: 1.6;
  font-size: 1rem;
}

.delete-button {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
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
  border-radius: 16px;
  padding: 2.5rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.verification-modal {
  max-width: 450px;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 700;
}

.modal-info {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1.5rem;
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

.verify-button,
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

.verify-button {
  background-color: #4CAF50;
  color: white;
}

.verify-button:hover:not(:disabled) {
  background-color: #45a049;
}

.verify-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  .mypage-container {
    padding: 1rem 0.5rem;
  }

  .mypage-card {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .info-item {
    padding: 1rem;
  }

  .modal-content {
    padding: 1.5rem;
  }

  .modal-buttons {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .verify-button,
  .confirm-button,
  .cancel-button {
    width: 100%;
  }

  .delete-section {
    padding: 1rem;
  }
}

/* 닉네임 수정 스타일 */
.info-item.editable {
  border-left-color: #ff9800;
}

.nickname-display {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.nickname-display span {
  flex: 1;
}

.edit-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: #2980b9;
  transform: translateY(-1px);
}

.nickname-edit {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.nickname-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #3498db;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.nickname-input:focus {
  outline: none;
  border-color: #2980b9;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.edit-buttons {
  display: flex;
  gap: 0.5rem;
}

.save-btn,
.cancel-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn {
  background: #4CAF50;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}

.nickname-error {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.nickname-success {
  color: #28a745;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  font-weight: 600;
}
</style>
