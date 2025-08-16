<template>
  <main class="page">
    <section class="card">
      <div class="logo">🔐</div>
      <h1 class="title">Fast Auth</h1>
      <p class="subtitle">Sign in with Google to continue</p>

      <button class="gbtn" @click="continueWithGoogle" :disabled="loading">
        <span v-if="loading" class="spinner" aria-hidden="true"></span>
        <img v-else src="../assets/google.png" width="20" height="20" alt="Google" />
        <span>{{ loading ? 'Connecting…' : 'Continue with Google' }}</span>
      </button>

      <p v-if="error" class="error">{{ error }}</p>

      <div class="scopes">
        <small>Requested scopes:</small>
        <ul>
          <li>Drive</li>
          <li>Calendar</li>
          <li>OpenID / Profile / Email</li>
        </ul>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  data() {
    return { loading: false, error: '' }
  },
  methods: {
    continueWithGoogle() {
      this.error = ''
      this.loading = true
      // backend can 303-redirect to Google from this URL
      window.location.href = 'http://localhost:8000/auth/google/url'
    }
  }
}
</script>

<style scoped>
/* Page background */
.page {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(900px 500px at 0% -10%, #cbe3fd33, transparent 60%),
    radial-gradient(900px 600px at 110% 110%, #b5ffd633, transparent 60%),
    linear-gradient(180deg, #0c1224 0%, #0f1428 100%);
  color: #e7eaf6;
}

/* Glass card */
.card {
  width: 100%;
  max-width: 480px;
  padding: 28px 24px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(10px);
  box-shadow:
    0 12px 30px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
  text-align: center;
}

/* Header */
.logo {
  width: 44px;
  height: 44px;
  margin: 0 auto 8px;
  display: grid;
  place-items: center;
  font-size: 22px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
}
.title {
  margin: 6px 0 4px;
  font-size: 1.7rem;
  letter-spacing: .2px;
}
.subtitle {
  margin: 0 0 18px;
  color: #c2c6d6;
  opacity: .95;
}

/* Google button */
.gbtn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1px solid #e6e8ef;
  background: #ffffff;
  color: #1f2330;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform .08s ease,
    box-shadow .2s ease,
    opacity .2s ease,
    border-color .2s ease;
  box-shadow: 0 8px 18px rgba(0,0,0,.18);
}
.gbtn:hover { transform: translateY(-1px); box-shadow: 0 12px 26px rgba(0,0,0,.22); }
.gbtn:active { transform: translateY(0); box-shadow: 0 6px 14px rgba(0,0,0,.24) inset; }
.gbtn:disabled { opacity: .7; cursor: not-allowed; }

/* Spinner */
.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(1turn); } }

/* Error + scopes */
.error { margin-top: 12px; color: #ff6b6b; font-weight: 500; }
.scopes { margin-top: 16px; font-size: .86rem; color: #cfd3e6; text-align: left; }
.scopes ul { margin: 6px 0 0; padding-left: 18px; }
</style>
