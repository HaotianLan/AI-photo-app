<template>
    <div class="register-container">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <input type="text" v-model="username" placeholder="用户名" required />
        </div>
        <div class="input-group">
          <input type="password" v-model="password" placeholder="密码" required />
        </div>
        <div class="input-group">
          <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
        </div>
        <div class="input-group">
          <input type="email" v-model="email" placeholder="邮箱" required />
        </div>
        <button type="submit">注册</button>
      </form>
      <p>已有账户? <router-link to="/login">登录</router-link></p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  //import { useRouter } from 'vue-router';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        errorMessage: ''
      };
    },
    methods: {
      async handleRegister() {
        // 检查密码和确认密码是否一致
        if (this.password !== this.confirmPassword) {
          alert('密码和确认密码不一致');
          return;
        }
  
        // 创建注册数据
        const registrationData = {
          username: this.username,
          password: this.password,
          email: this.email
        };
  
        try {
          // 发送注册请求
          const response = await axios.post('http://localhost:5001/register', registrationData);
  
          // 后端返回结果判断
          if (response.data.success) {
            // 注册成功，跳转到登录页面
            this.$router.push('/login');
          } else {
            // 如果返回账户名已存在，给用户提示
            this.errorMessage = '账户名已存在，请选择其他用户名';
          }
        } catch (error) {
          console.error(error);
          alert('注册失败，请稍后再试');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
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
  
  .error-message {
    color: red;
    margin-top: 10px;
  }
  </style>
  