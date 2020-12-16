<template>
  <div class="login box">
    <!--    <el-page-header @back="goBack" content="首页">-->
    <!--    </el-page-header>-->
    <img src="../static/image/1111.jpg" alt="" class="img1">
    <div class="login">
      <div class="login-title">
        <img src="../static/image/logo.png" alt="">
        <p>百知教育给你最优质的学习体验!</p>
      </div>
      <div class="login_box">
        <div class="title">
          <span @click="login_type=0">密码登录</span>
          <span @click="login_type=1">短信登录</span>
        </div>
        <div class="inp" v-if="login_type==0">
          <input type="text" placeholder="用户名 / 手机号码 / 邮箱" class="user" v-model="username">
          <input type="password" name="" class="pwd" placeholder="密码" v-model="password">
          <div id="geetest1"></div>
          <div class="rember">
            <p>
              <el-checkbox class="no" v-model="remember_me">记住密码</el-checkbox>
            </p>
            <p>忘记密码</p>
          </div>
          <el-button type="success" class="login_btn" @click="login_btn"
                     :disabled="!username || !password">登录
          </el-button>
          <p class="go_login">没有账号
            <router-link to="/sign_in">立即注册</router-link>
          </p>
        </div>
        <div class="inp" v-show="login_type==1">
          <input type="text" v-model="phone" placeholder="手机号码" class="user" @blur="check_phone">
          <input type="text" v-model="sms_code" class="pwd" placeholder="短信验证码">
          <el-button :disabled="disabled" @click="get_code" class="btn" type="primary" plain size="mini">
            {{ btntxt }}
          </el-button>
          <el-button type="success" class="login_btn" @click="login_message">登录</el-button>
          <span class="go_login">没有账号
                    <router-link to="/sign_in">立即注册</router-link>
                </span>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      login_type: 0,
      username: "",
      password: "",
      remember_me: false,
      phone: "",
      phone_flag: false,
      sms_code: "",
      disabled: false,
      time: 60,
      btntxt: "获取验证码",
    }
  },
  methods: {
    get_code() {
      if (this.phone_flag) {
        this.$axios({
          url: this.$settings.HOST + 'user/message/',
          method: 'get',
          params: {
            phone: this.phone,
          }
        }).then(response => {
          console.log(response)
        }).catch(error => {
          console.log(error)
        })
      }
      this.time = 60;
      this.timer();
    },
    timer() {
      if (this.time > 0) {
        this.disabled = true
        this.time--
        this.btntxt = this.time + "s"
        setTimeout(this.timer, 1000)
      } else {
        this.time = 0;
        this.btntxt = "发送验证码";
        this.disabled = false;
      }
    },

    login_message() {
      if (this.phone === '' || this.code === '') {
        this.$message({
          message: "手机号或验证码不能为空",
          type: 'error',
          duration: 2000,
          showClose: true,
        })
      }
      else if (this.phone_flag) {
        console.log(11111)
        this.$axios({
          url: this.$settings.HOST + 'user/login_message/',
          method: 'post',
          data: {
            phone: this.phone,
            sms_code: this.sms_code
          }
        }).then(response => {
          console.log(response.data, 207)
          localStorage.setItem('token', response.data.data.token)
          localStorage.setItem('username', response.data.data.username)
          localStorage.setItem('id', response.data.data.id)
          sessionStorage.setItem('token', response.data.data.token)
          sessionStorage.setItem('username', response.data.data.username)
          sessionStorage.setItem('id', response.data.data.id)
          let self = this;
          this.$alert("登录成功", "百知教育", {
            callback() {
              self.$router.push("/")
            }
          })
        }).catch(error => {
          console.log(error)
          this.$message({
            message: "登陆失败",
            type: 'error',
            duration: 2000,
            showClose: true,
          })
        })
      }
    },

    check_phone() {
      this.$axios({
        url: this.$settings.HOST + "user/check_phone_login/",
        method: 'post',
        data: {
          phone: this.phone,
        }
      }).then(response => {
        console.log(response)
        this.phone_flag = true
      }).catch(error => {
        console.log(error)
        this.$message({
          message: "手机号不正确",
          type: 'success',
          duration: 2000,
          showClose: true,
        })
      })
    },
    //    验证码判断
    // check_code() {
    //   this.$axios({
    //     url: this.$settings.HOST + "user/check_code_login/",
    //     method: 'post',
    //     data: {
    //       sms_code: this.sms_code,
    //     }
    //   }).then(response => {
    //     console.log(response)
    //     this.phone_flag = true
    //   }).catch(error => {
    //     console.log(error)
    //     this.$message({
    //       message: "验证码不正确",
    //       type: 'error',
    //       duration: 2000,
    //     })
    //   })
    //
    // },
    // 点击登录按钮时 获取滑块验证码
    login_btn() {
      this.$axios({
        url: this.$settings.HOST + "user/captcha/",
        method: 'get',
        params: {
          username: this.username,
        }
      }).then(res => {
        let data = JSON.parse(res.data);
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
          gt: data.gt,
          challenge: data.challenge,
          product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
          offline: !data.success, // 表示用户后台检测极验服务器是否宕机，一般不需要关注
          new_captcha: data.new_captcha
        }, this.handlerPopup);
      }).catch(error => {
        console.log(error);
      })
    },

    // 请求验证码的回调函数 完成验证码的验证码
    handlerPopup(captchaObj) {
      // 在回调函数中 this的指向会被改变
      let self = this;
      captchaObj.onSuccess(function () {
        let validate = captchaObj.getValidate();
        console.log(validate.geetest_challenge)
        self.$axios({
          url: self.$settings.HOST + "user/captcha/",
          method: "post",
          data: {
            geetest_challenge: validate.geetest_challenge,
            geetest_validate: validate.geetest_validate,
            geetest_seccode: validate.geetest_seccode
          },
        }).then(res => {
          console.log(res.data);
          // 如果滑块验证码的验证结果为True，则完成登录
          if (res.data.status) {
            self.user_login();
          }
        }).catch(error => {
          console.log(error);
        })
      })
      // 将验证码加到id为captcha的元素里
      document.getElementById("geetest1").innerHTML = "";
      captchaObj.appendTo("#geetest1");
    },
    // 用户登录请求
    user_login() {
      this.$axios({
        url: this.$settings.HOST + "user/login/",
        method: 'post',
        data: {
          username: this.username,
          password: this.password,
        }
      }).then(res => {
        // 判断是否记住密码  保存用户信息
        if (this.remember_me) {
          // 记住登录
          sessionStorage.clear();
          localStorage.token = res.data.token;
          localStorage.id = res.data.id;
          localStorage.username = res.data.username;
        } else {
          // 未记住登录
          localStorage.clear();
          sessionStorage.token = res.data.token;
          sessionStorage.id = res.data.id;
          sessionStorage.username = res.data.username;
        }

        this.$message({
          message: "恭喜你，登录成功",
          type: 'success',
          duration: 2000
        })
        // 登录成功后返回首页
        this.$router.push("/")
      }).catch(error => {
        console.log(error);
        this.$message.error("用户名或密码错误")
      })
    },
  }
}
</script>

<style scoped>
.box {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.box img {
  width: 100%;
  min-height: 100%;
}

.box .login {
  position: absolute;
  width: 500px;
  height: 400px;
  top: 0;
  left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -338px;
}

.login .login-title {
  width: 100%;
  text-align: center;
}

.login-title img {
  width: 190px;
  height: auto;
}

.login-title p {
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.login_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
  opacity: 0.85;
}

.login_box .title {
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}

.login_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  border-bottom: 2px solid #84cc39;
}

.inp {
  width: 350px;
  margin: 0 auto;
}

.inp input {
  border: 0;
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.btn {
  margin-top: 10px;
}

.inp input.user {
  margin-bottom: 16px;
}

.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}

.inp .rember p:first-of-type {
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  /*position: relative;*/
}

.inp .rember p:nth-of-type(2) {
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .rember input {
  outline: 0;
  width: 30px;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}

.inp .rember p span {
  display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
  /*left: 20px;*/

}

#geetest {
  margin-top: 20px;
}

.login_btn {
  width: 100%;
  height: 45px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 30px;
}

.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}

.inp .go_login span {
  color: #84cc39;
  cursor: pointer;
}
</style>