<!-- <template>
  <div class="auth-page">
    <RouterLink to="/" class="back-link">← To the Main</RouterLink>
    <div class="container">
      <h1 class="loading-text" v-if="!userName">Authorization processing...</h1>
      <div v-if="message" class="message">
        {{ message }}
      </div>
      <div v-if="userName" class="welcome">
        Welcome, <strong>{{ userName }}</strong>!
      </div>
      <img v-if="picUrl" :src="picUrl" class="avatar" />

      <div v-if="fileNames.length" class="files">
        <h2>Your files in Google Drive:</h2>
        <ul>
          <li v-for="file in fileNames" :key="file">{{ file }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      userName: '',
      picUrl: '',
      fileNames: [],
    };
  },
  mounted() {
    const queryParams = new URLSearchParams(window.location.search);
    const code = queryParams.get('code')
    const state = queryParams.get('state')

    if (code && state) {
      fetch('http://localhost:8000/auth/google/callback', {
        body: JSON.stringify({ code, state }),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
        .then(res => {
          if (!res.ok) {
            throw new Error('Internal server error')
          }
          return res.json()
        })
        .then(data => {
          this.picUrl = data.user.picture
          this.userName = data.user.name
          this.fileNames = data.files
        })
    } else {
      this.message = 'No code parameter';
    }
  },
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0f4ff, #e0f7fa);
  font-family: 'Inter', sans-serif;
}

.back-link {
  margin: 20px;
  text-decoration: none;
  color: #3f51b5;
  font-size: 16px;
  font-weight: 500;
  transition: color 0.3s;
}

.back-link:hover {
  color: #1a237e;
}

.container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
}

.loading-text {
  color: #333;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 25px;
  animation: fade 1.5s infinite;
}

@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.message {
  font-size: 18px;
  color: #616161;
  background-color: #ffffff;
  padding: 12px 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.welcome {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-radius: 12px;
  padding: 15px 30px;
  font-size: 20px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  margin-top: 15px;
}

.files {
  margin-top: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 15px 25px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: left;
  width: 100%;
  max-width: 500px;
}

.files h2 {
  font-size: 22px;
  margin-bottom: 10px;
  color: #3f51b5;
}

.files ul {
  list-style-type: disc;
  padding-left: 20px;
}

.files li {
  font-size: 16px;
  color: #333;
  margin-bottom: 5px;
}
</style> -->

<!-- Fancy rebuilt -->
<template>
  <div class="page">
    <RouterLink to="/" class="back">← Back</RouterLink>

    <section class="card">
      <!-- Loading state -->
      <div v-if="isLoading" class="loading">
        <div class="skeleton avatar"></div>
        <div class="skeleton line w-60"></div>
        <div class="skeleton line w-40"></div>
        <div class="spinner" aria-label="Loading"></div>
      </div>

      <!-- Error / info message -->
      <div v-else-if="message" class="notice">{{ message }}</div>

      <!-- Success -->
      <div v-else>
        <header class="header">
          <img v-if="picUrl" :src="picUrl" class="avatar" alt="Avatar" />
          <div v-else class="avatar initials">{{ initials }}</div>
          <div class="meta">
            <h1 class="title">Welcome</h1>
            <p class="subtitle"><strong>{{ userName }}</strong></p>
          </div>
        </header>

        <section v-if="files.length" class="files">
          <div class="files-head">
            <h2>Google Drive files</h2>
            <div class="count">{{ files.length }} total</div>
          </div>

          <ul class="file-list">
            <li v-for="(file, i) in paginatedFiles" :key="`${i}-${file}`" class="file-item">
              <span class="dot"></span>
              <span class="name" :title="file">{{ file }}</span>
            </li>
          </ul>

          <nav class="pager" v-if="totalPages > 1">
            <button class="pg-btn" :disabled="page === 1" @click="prevPage">Prev</button>
            <span class="pg-info">Page {{ page }} of {{ totalPages }}</span>
            <button class="pg-btn" :disabled="page === totalPages" @click="nextPage">Next</button>
          </nav>
        </section>

        <section v-else class="empty">
          <div class="empty-ico">📁</div>
          <p>No files found.</p>
        </section>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      userName: '',
      picUrl: '',
      files: [],
      isLoading: true,
      page: 1,
      pageSize: 8, // tweak page size here
    };
  },
  computed: {
    totalPages() {
      return Math.max(1, Math.ceil(this.files.length / this.pageSize));
    },
    paginatedFiles() {
      const start = (this.page - 1) * this.pageSize;
      return this.files.slice(start, start + this.pageSize);
    },
    initials() {
      if (!this.userName) return '🙂';
      return this.userName
        .split(' ')
        .map((x) => x[0]?.toUpperCase())
        .slice(0, 2)
        .join('') || '🙂';
    },
  },
  methods: {
    nextPage() {
      if (this.page < this.totalPages) this.page += 1;
    },
    prevPage() {
      if (this.page > 1) this.page -= 1;
    },
    async postCallback(code, state) {
      try {
        const res = await fetch('http://localhost:8000/auth/google/callback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code, state }),
        });
        if (!res.ok) {
          const t = await res.text();
          throw new Error(t || `Server error ${res.status}`);
        }
        const data = await res.json();
        // expecting: { user: { name, picture }, files: [...] }
        this.picUrl = data?.user?.picture || '';
        this.userName = data?.user?.name || 'User';
        this.files = Array.isArray(data?.files) ? data.files : [];
      } catch (e) {
        this.message = e?.message || 'Something went wrong';
      } finally {
        this.isLoading = false;
      }
    },
  },
  mounted() {
    const qs = new URLSearchParams(window.location.search);
    const code = qs.get('code');
    const state = qs.get('state');

    if (code && state) {
      this.postCallback(code, state);
    } else {
      this.isLoading = false;
      this.message = 'Missing OAuth params.';
    }
  },
};
</script>

<style scoped>
:root { color-scheme: light; }

.page {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: radial-gradient(800px 500px at 10% -10%, #eef2ff 40%, transparent 60%),
              radial-gradient(900px 600px at 110% 110%, #e0f7fa 40%, transparent 60%),
              #f7f8fb;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
  color: #0f172a;
}

.back {
  position: fixed;
  top: 18px;
  left: 18px;
  padding: 8px 10px;
  border-radius: 10px;
  text-decoration: none;
  color: #334155;
  border: 1px solid #e5e7eb;
  background: #fff;
  transition: transform .08s ease, box-shadow .2s ease;
}
.back:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(0,0,0,.08); }

.card {
  width: 100%;
  max-width: 760px;
  background: #fff;
  border: 1px solid #eaeef5;
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.loading {
  display: grid;
  place-items: center;
  gap: 10px;
  padding: 24px;
}

.skeleton {
  background: linear-gradient(90deg, #eef1f6, #f6f8fb, #eef1f6);
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite linear;
  border-radius: 12px;
}
.skeleton.avatar { width: 80px; height: 80px; border-radius: 50%; }
.skeleton.line { height: 14px; width: 80%; }
.w-60 { width: 60% !important; }
.w-40 { width: 40% !important; }
@keyframes shimmer { to { background-position: -200% 0; } }

.spinner {
  width: 20px; height: 20px;
  border: 2px solid #94a3b8;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(1turn); } }

.notice {
  padding: 14px 16px;
  border-radius: 12px;
  background: #fff7ed;
  color: #9a3412;
  border: 1px solid #fed7aa;
  text-align: center;
}

.header {
  display: grid;
  grid-template-columns: 80px 1fr;
  gap: 16px;
  align-items: center;
  padding: 6px;
  margin-bottom: 10px;
}
.avatar {
  width: 80px; height: 80px; border-radius: 50%;
  object-fit: cover;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 14px rgba(0,0,0,.08);
}
.avatar.initials {
  display: grid; place-items: center;
  background: #f1f5f9; color: #0f172a; font-weight: 700;
}
.meta .title { margin: 0; font-size: 1.25rem; color: #0f172a; }
.meta .subtitle { margin: 4px 0 0; color: #475569; }

.files {
  margin-top: 16px;
  border-top: 1px dashed #e5e7eb;
  padding-top: 16px;
}
.files-head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.files-head h2 { margin: 0; font-size: 1rem; color: #0f172a; }
.count { color: #64748b; font-size: .9rem; }

.file-list {
  list-style: none; padding: 0; margin: 0;
  display: grid; gap: 8px;
}
.file-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border: 1px solid #eef1f6; border-radius: 12px;
  background: #fff;
  transition: transform .06s ease, box-shadow .2s ease, border-color .2s ease;
}
.file-item:hover {
  transform: translateY(-1px);
  border-color: #e5e7eb;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06);
}
.file-item .dot {
  width: 8px; height: 8px; border-radius: 50%; background: #0ea5e9; flex: 0 0 auto;
}
.file-item .name {
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1 1 auto;
  color: #0f172a;
}

.pager {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  margin-top: 14px;
}
.pg-btn {
  padding: 8px 12px; border-radius: 10px; border: 1px solid #e5e7eb; background: #fff;
  color: #0f172a; cursor: pointer; font-weight: 600;
  transition: transform .06s ease, box-shadow .2s ease, opacity .2s ease;
}
.pg-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 14px rgba(0,0,0,.06); }
.pg-btn:disabled { opacity: .5; cursor: not-allowed; box-shadow: none; transform: none; }
.pg-info { color: #475569; font-size: .92rem; }

.empty {
  display: grid; place-items: center; gap: 6px;
  padding: 30px 10px; color: #64748b;
}
.empty-ico { font-size: 28px; }
</style>
