<template>
    <div class="login-container">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <input type="text" v-model="username" placeholder="用户名" required />
        </div>
        <div class="input-group">
          <input type="password" v-model="password" placeholder="密码" required />
        </div>
        <button type="submit">登录</button>
      </form>
      <p>还没有账户? <router-link to="/register">注册</router-link></p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async handleLogin() {
        try {
          // 发送POST请求到后端
          const response = await axios.post('http://localhost:5001/login', {
            username: this.username,
            password: this.password
          });
  
          // 如果请求成功，接收返回的JWT并存储
          const jwt = response.data.token;
  
          // 存储JWT在本地存储（localStorage）
          localStorage.setItem('jwt', jwt);
          localStorage.setItem('isAuthenticated', 'true');
  
          // 跳转到首页或其他页面
          console.log('跳转到 /authenticated');
          this.$router.push('/authenticated'); // 假设跳转到/dashboard
        } catch (error) {
          console.error('登录失败:', error);
          alert('登录失败，请检查用户名、邮箱或密码');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    /* Flexbox 设置 */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 让容器的高度填满视口 */
  }
  
  h2 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .input-group {
    margin-bottom: 10px;
  }
  
  input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
  }
  
  p {
    text-align: center;
    margin-top: 10px;
  }
  </style>
  
  