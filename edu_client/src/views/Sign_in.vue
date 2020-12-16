<template>
  <el-container>
    <div class="box">
      <el-header>
        <router-link to="/" class="shou">首页</router-link>
      </el-header>
      <img src="../static/image/1111.jpg" alt="">
      <div class="register">
        <el-main>
          <div class="register_box">
            <div class="register-title">百知教育在线平台注册</div>
            <div class="inp">
              <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
              <input v-model="password" type="password" placeholder="登录密码" class="user" @blur="check_password">
              <div id="geetest"></div>
              <div class="sms-box">
                <el-input v-model="sms_code" type="text" maxlength="6" placeholder="输入验证码" class="user"></el-input>
                <el-button :disabled="disabled" @click="get_code" class="sendcode" type="primary" plain size="mini">
                  {{ btntxt }}
                </el-button>
              </div>
              <el-button type="success" class="register_btn" @click="re_button" :disabled="!phone || !password || !sms_code">注册</el-button>
              <p class="go_login">已有账号
                <router-link to="/login">直接登录</router-link>
              </p>
            </div>
          </div>
        </el-main>
      </div>
    </div>
  </el-container>
</template>
<script>
export default {
  name: "Sign_in",
  data() {
    return {
      phone: '',
      password: '',
      sms_code: "",
      register_flag: false,
      disabled: false,
      time: 60,
      btntxt: "发送验证码",
    }
  },

  methods: {
    re_button() {
      if (this.phone === "" || this.password === "" || this.sms_code === "") {
        this.$message({
          message: "账号或密码或验证码不能为空",
          type: 'warning',
          duration: 2000,
          showClose: true,
        })
      } else if (this.register_flag) {
        this.$axios({
          url: this.$settings.HOST + 'user/sign_in/',
          method: 'post',
          data: {
            phone: this.phone,
            password: this.password,
            sms_code: this.sms_code,
          }
        }).then(res => {
          console.log(58, res.data);
          //保存成功，自动登录
          localStorage.clear()
          localStorage.setItem('username', this.username)
          localStorage.setItem('password', this.password)
          localStorage.setItem('phone', this.phone)
          localStorage.setItem('token', res.data.token)
          sessionStorage.setItem('token', res.data.token)
          let self = this;
          self.$alert("注册成功", "星河璀璨", {
            callback() {
              self.$router.push("/")
            }
          })
        }).catch(error => {
          console.log(76, error),
              this.$message({
                message: '注册失败',
                type: 'warning',
                duration: 2000,
                showClose: true,
              })
        })
      }
    },
    //检查手机号是否唯一
    check_phone() {
      let phoneNumber = this.phone;
      // 前端
      let reg = /^1[3-9][0-9]{9}$/;
      if (!reg.test(phoneNumber)) { // 前端检测手机号长度是否符合要求
        this.$message.error('手机号格式不对或为空');
        return false;
      }
      // 如果前端验证手机号长度没问题，就向后端发起请求
      this.$axios({
        url: this.$settings.HOST + 'user/check_phone/',
        method: 'post',
        data: {
          phone: this.phone
        }
      }).then(res => {
        console.log(104, res.data)
        this.register_flag = true
      }).catch(error => {
        console.log(86, error.response.data)
        this.$message.error("手机号存在");
      })
    },
    check_password() {
      if (this.password === "") {
        this.$message.error('密码格式或位数不对')
      }
    },
    get_code() {
      this.$axios({
        url: this.$settings.HOST + "user/message/",
        method: 'get',
        params: {
          phone: this.phone,

        }
      }).then(res => {
        console.log(res);
      }).catch(error => {
        console.log(error);
        this.$message({
          message: "验证码错误",
          type: 'warning',
          duration: 2000,
          showClose: true,
        })
      })
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

.box .register {
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

.shou {
  font-size: 20px;
  float: right;
  margin-right: 20px;
  margin-top: 15px;
}

.register .register-title {
  width: 100%;
  font-size: 24px;
  text-align: center;
  padding-top: 30px;
  padding-bottom: 30px;
  color: #4a4a4a;
  letter-spacing: .39px;
}

.register-title img {
  width: 190px;
  height: auto;
}

.register-title p {
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: .29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.register_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
  opacity: 0.85;
}

.register_box .title {
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

.register_box .title span:nth-of-type(1) {
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

.register_btn {
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

.sms-box {
  position: relative;
}

.sms-btn {
  font-size: 14px;
  color: #ffc210;
  letter-spacing: .26px;
  position: absolute;
  right: 16px;
  top: 10px;
  cursor: pointer;
  overflow: hidden;
  background: #fff;
  border-left: 1px solid #484848;
  padding-left: 16px;
  padding-bottom: 4px;
}

.sendcode {
  margin-top: 5px;
}
</style>