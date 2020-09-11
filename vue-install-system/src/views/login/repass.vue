<template>
  <div class="app-container common-list-page">
    <el-form
      :model="resetForm"
      :rules="resetFormRules"
      ref="resetForm"
      status-icon
      label-width="100px"
    >
      <el-form-item label="用户名:" prop="text" :disabled="true">
        <el-col :span="8">
        <el-input type="text" v-model="resetForm.username" auto-complete="off" :disabled="true" ></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="旧密码:" prop="password">
        <el-col :span="8">
        <el-input type="password" v-model="resetForm.password" auto-complete="off" ></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="新密码:" prop="newpwd">
        <el-col :span="8">
        <el-input type="password" v-model="resetForm.newpwd" auto-complete="off"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item label="确认密码:" prop="newpassword1">
        <el-col :span="8">
        <el-input type="password" v-model="resetForm.newpassword1" auto-complete="off"></el-input>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-col :span="8">
        <el-button type="primary" @click.native.prevent="toAmend">确认修改</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import { fetchList, fetchPv, createArticle, updateArticle,statustag,repassArticle } from '@/api/article'
  export default {
    data() {
      var validatePass = (rule, value, callback) => {
        if (!value) {
          callback(new Error("请输入新密码"));
        } else if (value.toString().length < 6 || value.toString().length > 18) {
          callback(new Error("密码长度为6-18位"));
        } else {
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === "") {
          callback(new Error("请再次输入密码"));
        } else if (value !== this.resetForm.newpwd) {
          callback(new Error("两次输入密码不一致!"));
        } else {
          callback();
        }
      };
      return {
        resetForm: {
          //传给后台所需要的参数
          newpassword1: "",
          password: "",
          username: ""//此处只是后台需要的字段而已，如果前期有公用cookie里面有获取并且保存过，现在需要另外调用进来，具体的获取方法就看个人了
        },
        resetFormRules: {
          password: [
            { required: true, message: "请输入旧密码", trigger: 'blur' }
          ],
          newpwd: [
            { required: true, validator: validatePass, trigger: 'blur' }
          ],
          newpassword1: [
            { required: true, validator: validatePass2, trigger: "blur" }
          ]
        }
      };
    },
    methods: {
      getCookie: function (cname) {
        var name = cname + "=";
        var x = '123';
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
          var c = ca[i];
          this.resetForm.username = c.split('=')[1];
          while (c.charAt(0) == ' ') c = c.substring(1);
          if (c.indexOf(name) != -1){
            return c.substring(name.length, c.length);
          }
        }
        return x;
      },
      toAmend() {
        this.$refs.resetForm.validate(valid => {
          if (valid) {
            repassArticle(this.resetForm)
              .then(res => {
                if(res.code === 20002){
                  this.$message({
                    message: res.msg,
                    type: "error",
                    duration: "2000"
                  });
                  return false;
                }
                if (res.code === 20000) {
                  this.$message.success("修改成功,3秒后跳转到登录页！");
                  setTimeout(() => {
                    this.logout();//调用跳转到登陆页的方法
                  }, 3000);
                }
                ic
              })
              .catch(() => {});
          }
        });
      },
      //这是修改成功后重新返回登陆页的方法，看个人需要自行调整
      async logout() {
        await this.$store.dispatch("user/logout");
        this.$router.push(`/login`);
      }
    },
    created() {
      this.getCookie()
    },
  };
</script>

<style lang="scss" scoped>
  .el-form {
    width: 60%;
    margin: 50px auto 0;
    text-align: center;
    button {
      margin: 10px 0 0;
    }
  }
</style>
