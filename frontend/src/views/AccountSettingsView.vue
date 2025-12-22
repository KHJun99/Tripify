<template>
  <div class="mypage-wrapper">
    <!-- 비밀번호 확인 모달 (일반 로그인 사용자만) -->
    <transition name="modal-fade">
      <div v-if="showPasswordVerification" class="modal-backdrop">
        <div class="modal-card verification-modal">
          <div class="modal-header">
            <div class="icon-circle lock-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            </div>
            <h3 class="modal-title">본인 확인</h3>
            <p class="modal-desc">
              개인정보 보호를 위해 비밀번호를 입력해주세요.
            </p>
          </div>

          <div class="modal-body">
            <div class="input-group">
              <input
                type="password"
                v-model="verifyPassword"
                placeholder="비밀번호 입력"
                class="clean-input"
                @keyup.enter="handlePasswordVerification"
                autofocus
              />
            </div>
            <p v-if="verifyError" class="error-text">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
              {{ verifyError }}
            </p>
          </div>

          <div class="modal-footer">
            <button
              @click="handleCancelVerification"
              class="btn btn-ghost"
              :disabled="isVerifying"
            >
              취소
            </button>
            <button
              @click="handlePasswordVerification"
              class="btn btn-primary"
              :disabled="isVerifying || !verifyPassword"
            >
              {{ isVerifying ? '확인 중...' : '확인하기' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 마이페이지 컨텐츠 -->
    <div v-if="isVerified" class="content-container">
      <div class="dashboard-grid">
        
        <!-- 프로필 사이드바 -->
        <aside class="profile-sidebar">
          <div class="card profile-card">
            <div class="profile-avatar">
              <span class="avatar-text">{{ user?.nickname?.charAt(0) || user?.username?.charAt(0) || 'U' }}</span>
            </div>
            
            <div class="profile-header">
              <h2 class="profile-name">
                {{ user?.nickname || '닉네임 없음' }}
                <button @click="startEditNickname" class="btn-icon-edit" title="닉네임 수정">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
              </h2>
              <p class="profile-email">{{ user?.email }}</p>
            </div>
            
            <div class="profile-badges">
              <span class="badge" :class="getLoginTypeClass(user?.login_type)">
                {{ getLoginTypeLabel(user?.login_type) }}
              </span>
            </div>

            <transition name="slide-fade">
              <div v-if="isEditingNickname" class="nickname-edit-box">
                <input 
                  v-model="editingNickname" 
                  type="text" 
                  class="clean-input sm"
                  placeholder="새 닉네임"
                  maxlength="50"
                  @keyup.enter="saveNickname"
                  @keyup.esc="cancelEditNickname"
                  ref="nicknameInputRef"
                />
                <div class="edit-actions">
                  <button @click="saveNickname" class="btn btn-primary btn-sm" :disabled="isSavingNickname">저장</button>
                  <button @click="cancelEditNickname" class="btn btn-ghost btn-sm">취소</button>
                </div>
                <p v-if="nicknameError" class="error-text sm">{{ nicknameError }}</p>
                <p v-if="nicknameSuccess" class="success-text sm">{{ nicknameSuccess }}</p>
              </div>
            </transition>
            
            <div class="profile-meta">
              <div class="meta-item">
                <span class="label">가입일</span>
                <span class="value">{{ formatDate(user?.created_at) }}</span>
              </div>
            </div>
          </div>
        </aside>

        <!-- 설정 메인 -->
        <main class="settings-main">
          
          <!-- 회원 정보 섹션 -->
          <section class="card settings-card">
            <div class="card-header">
              <h3 class="card-title">내 정보</h3>
            </div>
            <div class="card-body">
              <div class="info-list">
                <div class="info-row">
                  <span class="info-label">아이디</span>
                  <span class="info-value">{{ user?.username }}</span>
                </div>
                <div class="divider"></div>
                <div class="info-row" v-if="user?.preferred_region">
                  <span class="info-label">선호 지역</span>
                  <span class="info-value">{{ user.preferred_region }}</span>
                </div>
                <div class="info-row" v-if="user?.travel_style">
                  <span class="info-label">여행 스타일</span>
                  <span class="info-value">{{ user.travel_style }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- 비밀번호 변경 섹션 -->
          <section class="card settings-card">
            <div class="card-header">
              <h3 class="card-title">보안 설정</h3>
            </div>
            
            <div class="card-body">
              <div v-if="isNormalLogin" class="form-container">
                <form @submit.prevent="handlePasswordChange">
                  <div class="form-group">
                    <label>현재 비밀번호</label>
                    <input
                      type="password"
                      v-model="passwordForm.currentPassword"
                      class="clean-input"
                      placeholder="••••••••"
                    />
                  </div>
                  
                  <div class="form-row two-col">
                    <div class="form-group">
                      <label>새 비밀번호</label>
                      <input
                        type="password"
                        v-model="passwordForm.newPassword"
                        class="clean-input"
                        placeholder="8자 이상"
                      />
                    </div>
                    <div class="form-group">
                      <label>새 비밀번호 확인</label>
                      <input
                        type="password"
                        v-model="passwordForm.newPasswordConfirm"
                        class="clean-input"
                        placeholder="다시 입력"
                      />
                    </div>
                  </div>

                  <div class="form-actions">
                    <p v-if="passwordError" class="error-text">{{ passwordError }}</p>
                    <p v-if="passwordSuccess" class="success-text">{{ passwordSuccess }}</p>
                    <button
                      type="submit"
                      class="btn btn-dark"
                      :disabled="isChangingPassword || !isPasswordFormValid"
                    >
                      {{ isChangingPassword ? '변경 중...' : '비밀번호 변경' }}
                    </button>
                  </div>
                </form>
              </div>

              <div v-else class="social-notice">
                <div class="notice-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                </div>
                <p>소셜 로그인 계정(카카오/구글)은 해당 플랫폼에서 비밀번호를 관리합니다.</p>
              </div>
            </div>
          </section>

          <!-- 회원탈퇴 섹션 -->
          <section class="card settings-card danger-zone">
            <div class="card-header">
              <h3 class="card-title">계정 관리</h3>
            </div>
            <div class="card-body">
              <div class="danger-row">
                <div class="danger-info">
                  <h4>회원 탈퇴</h4>
                  <p>탈퇴 시 모든 데이터가 영구적으로 삭제되며 복구할 수 없습니다.</p>
                </div>
                <button
                  @click="showDeleteConfirmation = true"
                  class="btn btn-outline-danger"
                  :disabled="isDeleting"
                >
                  회원 탈퇴
                </button>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>

    <!-- 회원탈퇴 확인 모달 -->
    <transition name="modal-fade">
      <div v-if="showDeleteConfirmation" class="modal-backdrop" @click.self="closeDeleteModal">
        <div class="modal-card delete-modal">
          <div class="modal-header">
            <div class="icon-circle danger-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            </div>
            <h3 class="modal-title">정말 떠나시겠습니까?</h3>
            <p class="modal-desc">
              계정을 삭제하면 복구가 불가능합니다.
            </p>
          </div>

          <div class="modal-body">
            <div v-if="isNormalLogin" class="input-group">
              <label class="input-label">비밀번호 확인</label>
              <input
                type="password"
                v-model="deletePassword"
                placeholder="현재 비밀번호 입력"
                class="clean-input"
                @keyup.enter="handleDeleteAccount"
              />
            </div>
            <p v-if="deleteError" class="error-text center">{{ deleteError }}</p>
          </div>

          <div class="modal-footer">
            <button
              @click="closeDeleteModal"
              class="btn btn-ghost"
              :disabled="isDeleting"
            >
              취소
            </button>
            <button
              @click="handleDeleteAccount"
              class="btn btn-danger"
              :disabled="isDeleting || (isNormalLogin && !deletePassword)"
            >
              {{ isDeleting ? '처리 중...' : '탈퇴하기' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
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
    normal: '일반 회원',
    kakao: 'KAKAO',
    google: 'GOOGLE',
  }
  return labels[type] || '일반 회원'
}

const getLoginTypeClass = (type) => {
  const classes = {
    normal: 'badge-normal',
    kakao: 'badge-kakao',
    google: 'badge-google',
  }
  return classes[type] || 'badge-normal'
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
/* Reset */
* {
  box-sizing: border-box;
}

.mypage-wrapper {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 3rem 1rem;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color: #333;
}

.content-container {
  max-width: 1100px;
  margin: 0 auto;
}

/* Grid Layout */
.dashboard-grid {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

/* Common Card */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  border: 1px solid #f0f0f0;
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fff;
}

.card-title {
  font-size: 1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

/* Profile Sidebar */
.profile-card {
  padding: 3rem 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  background-color: #e0e4ff;
  color: #5a67d8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.profile-header {
  margin-bottom: 1rem;
}

.profile-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-icon-edit {
  background: none;
  border: none;
  color: #a0aec0;
  cursor: pointer;
  padding: 4px;
  display: flex;
  transition: color 0.2s;
}

.btn-icon-edit:hover {
  color: #4a5568;
}

.profile-email {
  color: #718096;
  font-size: 0.95rem;
  margin: 0;
}

.profile-badges {
  margin-bottom: 2rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
}

.badge-normal { background: #edf2f7; color: #4a5568; }
.badge-kakao { background: #fee500; color: #191919; }
.badge-google { background: #fff; border: 1px solid #e2e8f0; color: #4a5568; }

.profile-meta {
  width: 100%;
  border-top: 1px solid #f0f0f0;
  padding-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

.meta-item {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.meta-item .label { color: #a0aec0; }
.meta-item .value { color: #4a5568; font-weight: 500; }

/* Settings Main */
.settings-main {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.8rem;
  color: #718096;
  font-weight: 600;
}

.info-value {
  font-size: 1.1rem;
  color: #2d3748;
  font-weight: 500;
}

.divider {
  height: 1px;
  background-color: #f0f0f0;
  width: 100%;
}

/* Forms & Inputs */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.5rem;
}

.form-row.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.clean-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background-color: #fff;
}

.clean-input:focus {
  outline: none;
  border-color: #5a67d8;
  box-shadow: 0 0 0 3px rgba(90, 103, 216, 0.1);
}

.clean-input.sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
}

/* Buttons */
.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #5a67d8;
  color: white;
}
.btn-primary:hover:not(:disabled) { background-color: #4c51bf; }

.btn-dark {
  background-color: #2d3748;
  color: white;
}
.btn-dark:hover:not(:disabled) { background-color: #1a202c; }

.btn-ghost {
  background: transparent;
  color: #718096;
}
.btn-ghost:hover:not(:disabled) { background-color: #f7fafc; }

.btn-danger {
  background-color: #e53e3e;
  color: white;
}
.btn-danger:hover:not(:disabled) { background-color: #c53030; }

.btn-outline-danger {
  background: white;
  border: 1px solid #e53e3e;
  color: #e53e3e;
}
.btn-outline-danger:hover:not(:disabled) {
  background-color: #fff5f5;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}

/* Danger Zone */
.danger-zone {
  border: 1px solid #fed7d7;
  background-color: #fff5f5;
}

.danger-zone .card-header {
  background-color: transparent;
  border-bottom: 1px solid #fed7d7;
}

.danger-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.danger-info h4 {
  margin: 0 0 0.25rem 0;
  color: #c53030;
  font-size: 1rem;
}

.danger-info p {
  margin: 0;
  color: #c53030;
  font-size: 0.9rem;
  opacity: 0.8;
}

/* Social Notice */
.social-notice {
  background-color: #f7fafc;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: #718096;
  font-size: 0.95rem;
}

/* Modals */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}

.modal-card {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  overflow: hidden;
}

.modal-header {
  padding: 2rem 1.5rem 1rem;
  text-align: center;
}

.icon-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}
.lock-icon { background: #ebf4ff; color: #5a67d8; }
.danger-icon { background: #fff5f5; color: #e53e3e; }

.modal-title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  color: #2d3748;
}

.modal-desc {
  margin: 0;
  color: #718096;
  font-size: 0.95rem;
}

.modal-body {
  padding: 1rem 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem 1.5rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* Transitions */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.slide-fade-enter-active { transition: all 0.3s ease; }
.slide-fade-leave-active { transition: all 0.2s ease; }
.slide-fade-enter-from, .slide-fade-leave-to { transform: translateY(-5px); opacity: 0; }

.nickname-edit-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  margin-bottom: 1rem;
}
.edit-actions { display: flex; gap: 0.5rem; justify-content: center; }
.error-text { color: #e53e3e; font-size: 0.85rem; margin-top: 0.5rem; text-align: center; }
.error-text.sm { font-size: 0.8rem; }
.success-text { color: #38a169; font-size: 0.85rem; margin-top: 0.5rem; text-align: center; }
.success-text.sm { font-size: 0.8rem; }
</style>