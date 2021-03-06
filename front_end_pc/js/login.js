var vm = new Vue({
    el: '#app',

    data: {
        host: host,
        error_username: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        username: '',
        password: '',
        remember: false
    },

    methods: {
        // 获取url查询字符串参数值
        get_query_string: function (name) {
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
            var r = window.location.search.substr(1).match(reg);
            if (r !== null) {
                return decodeURI(r[2]);
            }
            return null;
        },

        // 检查用户名是否合法
        check_username: function () {
            if (!this.username) {
                this.error_username = true;
            } else {
                this.error_username = false;
            }
        },

        // 检查密码是否合法
        check_pwd: function () {
            if (!this.password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },

        // 表单提交: 执行登录操作
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            if (this.error_username === false && this.error_pwd === false) {
                axios.post(this.host + '/login/', {
                    username: this.username,
                    password: this.password
                })
                    .then(response => {
                        sessionStorage.clear();
                        localStorage.clear();
                        if (this.remember) {
                            localStorage.token = response.data.token;
                            localStorage.username = response.data.username;
                            localStorage.user_id = response.data.user_id;
                        } else {
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                        }
                        var return_url = this.get_query_string('next');
                        if (!return_url) {
                            return_url = '/index.html'
                        }
                        location.href = return_url;
                    })
                    .catch(error => {
                        if (error.data.status === 400) {
                            this.error_pwd_message = '账号或者密码错误'
                        } else {
                            this.error_pwd_message = '服务器错误'
                        }
                        this.error_pwd = true;
                    })
            }
        },

        // qq登录
        qq_login: function () {
            var next = this.get_query_string('next') || '/';
            axios.get(this.host + '/oauth/qq/authorization/?next=' + next)
                .then(response => {
                    location.href = response.data.login_url;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        }
    }
});
