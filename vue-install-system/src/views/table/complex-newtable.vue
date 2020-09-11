<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.title" :placeholder="$t('table.title')" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!--<el-select v-model="listQuery.importance" :placeholder="$t('table.importance')" clearable style="width: 90px" class="filter-item">-->
      <!--<el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />-->
      <!--</el-select>-->
      <el-select v-model="listQuery.type" :placeholder="$t('table.type')" clearable class="filter-item" style="width: 130px">
        <!--<el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />-->
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
      </el-select>
      <!--<el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">-->
      <!--<el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />-->
      <!--</el-select>-->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        {{ $t('table.search') }}
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        {{ $t('table.add') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        {{ $t('table.export') }}
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        {{ $t('table.reviewer') }}
      </el-checkbox>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column :label="$t('table.id')" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.date')" width="170px" align="center">
        <template slot-scope="{row}">
          <span>{{ dateFormat('YYYY-mm-dd HH:MM:SS',row.timestamp) }}</span>
          <!--<span>{{ row.timestamp }}</span>-->
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.nodehostip')" min-width="120px"  align="center">
        <template slot-scope="{row}">
          <span class="link-type">{{ row.nodeip }}</span>
          <!--<el-tag>{{ row.type | typeFilter }}</el-tag>-->
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.managerAdd')" min-width="120px"  align="center">
        <template slot-scope="{row}">
          <span class="link-type">{{ row.ipmiadd }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.title')" min-width="120px"  align="center">
        <template slot-scope="{row}">
          <span class="link-type">{{ row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.readings')" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.versions }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.author')" width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.author }}</span>
          <!--<span>{{ user.name }}</span>-->
        </template>
      </el-table-column>
      <!--审核人开关-->
      <!--<el-table-column v-if="showReviewer" :label="$t('table.reviewer')" width="110px" align="center">-->
      <!--<template slot-scope="{row}">-->
      <!--<span style="color:red;">{{ row.reviewer }}</span>-->
      <!--</template>-->
      <!--</el-table-column>-->
      <!--<el-table-column :label="$t('table.importance')" width="80px">-->
      <!--<template slot-scope="{row}">-->
      <!--<svg-icon v-for="n in +row.importance" :key="n" icon-class="star" class="meta-item__icon" />-->
      <!--</template>-->
      <!--</el-table-column>-->
      <!--<el-table-column :label="$t('table.readings')" align="center" width="95">-->
      <!--<template slot-scope="{row}">-->
      <!--&lt;!&ndash;<span v-if="row.pageviews" class="link-type" @click="handleFetchPv(row.pageviews)">{{ row.pageviews }}</span>&ndash;&gt;-->
      <!--<span v-else>0</span>-->
      <!--</template>-->
      <!--</el-table-column>-->
      <el-table-column :label="$t('table.status')" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.status | statusFilter">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('table.actions')" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <!--编辑开关-->
          <!--<el-button type="primary" size="mini" @click="handleUpdate(row)">-->
          <!--{{ $t('table.edit') }}-->
          <!--</el-button>-->
          <!--<el-button v-if="row.status!='0'" size="mini" type="warning" @click="handleData(row.id);handleModifyStatus(row,'成功')">-->
          <el-button v-if="row.status!='0'" size="mini" type="warning" @click="handleData(row.id,row.nodeip)">
            {{ $t('table.publish') }}
          </el-button>

          <!--<el-button v-if="row.status!='1'" size="mini" @click="handleModifyStatus(row,'draft')">-->
          <!--{{ $t('table.draft') }}-->
          <!--</el-button>-->
          <!--<el-button v-if="row.status!='2'" size="mini" type="danger" @click="handleDelete(row,$index)">-->
          <!--{{ $t('table.delete') }}-->
          <!--</el-button>-->
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item :label="$t('table.type')" prop="type">
          <el-select v-model="temp.type" class="filter-item" placeholder="请选择系统版本">
            <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('table.nodehostip')" prop="nodeip">
          <el-input v-model="temp.nodeip" />
        </el-form-item>
        <el-form-item :label="$t('table.nodegateway')" prop="nodegate">
          <el-input v-model="temp.nodegate" />
        </el-form-item>
        <el-form-item :label="$t('table.nodenetmask')" prop="nodemark" >
          <el-input v-model="temp.nodemark" placeholder="255.255.255.0"/>
        </el-form-item>
        <!--<el-form-item :label="$t('table.managerAdd')" prop="ipmi">-->
          <!--<el-input v-model="temp.ipmi" />-->
        <!--</el-form-item>-->
        <!--<el-form-item :label="$t('table.ippass')" prop="ipmipass">-->
          <!--<el-input v-model="temp.ipmipass" />-->
        <!--</el-form-item>-->
        <el-form-item :label="$t('table.title')" prop="title">
          <el-input v-model="temp.title" placeholder="AA:BB:CC:DD:EE:FF"/>
        </el-form-item>
        <el-form-item :label="$t('table.remark')">
          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="系统更换" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('table.cancel') }}
        </el-button>
        <el-button type="primary" v-loading.fullscreen.lock="fullscreenLoading" @click="dialogStatus==='create'?createData():updateData()">
          {{ $t('table.confirm') }}
        </el-button>
      </div>
    </el-dialog>

    <!--<el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">-->
    <!--<el-table :data="pvData" border fit highlight-current-row style="width: 100%">-->
    <!--<el-table-column prop="key" label="Channel" />-->
    <!--<el-table-column prop="pv" label="Pv" />-->
    <!--</el-table>-->
    <!--<span slot="footer" class="dialog-footer">-->
    <!--<el-button type="primary" @click="dialogPvVisible = false">{{ $t('table.confirm') }}</el-button>-->
    <!--</span>-->
    <!--</el-dialog>-->
  </div>
</template>

<script>
  import { fetchList, fetchPv, createArticle, updateArticle,statustag } from '@/api/article'
  import { validateIP,validateMAC,checkMask } from '@/api/datavalid'
  import waves from '@/directive/waves' // waves directive
  import { parseTime } from '@/utils'
  import Pagination from '@/components/Pagination' // secondary package based on el-pagination
  import moment from 'moment'

  export default {
    name: 'ComplexTable',
    components: { Pagination },
    directives: { waves },
    filters: {
      statusFilter(status) {
        const statusMap = {
          "成功": 'success',
          "失败": 'danger',
          "安装中": 'warning'
        }
        return statusMap[status]
      },
      typeFilter(type) {
        return this.calendarTypeKeyValue[type]
      },

    },
    data() {
      return {
        tableKey: 0,
        list: null,
        total: 0,
        listLoading: true,
        fullscreenLoading: false,
        timer: '',
        listQuery: {
          page: 1,
          limit: 20,
          importance: undefined,
          title: undefined,
          type: undefined,
          sort: '+id'
        },
        calendarTypeOptions: [
          { key: 'CN', display_name: '中国' },
          { key: 'US', display_name: 'USA' },
          { key: 'JP', display_name: 'Japan' },
          { key: 'EU', display_name: 'Eurozone' }
        ],
        importanceOptions: [1, 2, 3],
        sortOptions: [{ label: '升序', key: '+id' }, { label: '降序', key: '-id' }],
        statusOptions: ['成功', '失败', '删除'],
        showReviewer: false,
        temp: {
          id: undefined,
          importance: 1,
          remark: '',
          timestamp: moment().format('YYYY-MM-DD HH:mm:ss'),
          title: '',
          ipmi: '',
          author: '',
          nodegate: '',
          nodemark: '',
          ipmipass: '',
          tempstat: '1',
          nodeip: '',
          type: '',
          status: '安装中'
        },
        dialogFormVisible: false,
        dialogStatus: '',
        textMap: {
          update: 'Edit',
          create: '安装操作系统之前请联系IT部开通DHCP中继'
        },
        dialogPvVisible: false,
        pvData: [],
        rules: {
          type: [{ required: true, message: 'type is required', trigger: 'change' }],
          // timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
          title: [{ required: true, message: 'mac不能为空', trigger: 'blur' },{ validator: validateMAC, trigger: 'blur' },],
          ipmi: [{ required: true, message: 'ipmi不能为空', trigger: 'blur' },{ validator: validateIP, trigger: 'blur' },],
          ipmipass: [{ required: true, message: 'ipmi密码不能为空', trigger: 'blur' }],
          nodeip: [{ required: true, message: '服务器ip不能为空', trigger: 'blur' },{ validator: validateIP, trigger: 'blur' },],
          nodegate: [{ required: true, message: '服务器网关不能为空', trigger: 'blur' },{ validator: validateIP, trigger: 'blur' },],
          nodemark: [{ required: true, message: '服务器掩码不能为空', trigger: 'blur' }]
        },
        downloadLoading: false
      }
    },
    created() {
      this.listQuery.page = 1
      this.getList()
      this.getCookie()
    },
    methods: {
      getCookie: function (cname) {
        var name = cname + "=";
        var x = '';
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
          var c = ca[i];
          x = c.split('=')[1];
          while (c.charAt(0) == ' ') c = c.substring(1);
          if (c.indexOf(name) != -1){
            return c.substring(name.length, c.length);
          }
        }
        return x;
      },
      calendarTypeKeyValue (){
        return this.calendarTypeOptions.reduce((acc, cur) => {
          acc[cur.key] = cur.display_name
          return acc
        }, {})
      },
      dateFormat(fmt, date) {
        let ret="";
        date=new Date(date);
        const opt = {
          'Y+': date.getFullYear().toString(), // 年
          'm+': (date.getMonth() + 1).toString(), // 月
          'd+': date.getDate().toString(), // 日
          'H+': date.getHours().toString(), // 时
          'M+': date.getMinutes().toString(), // 分
          'S+': date.getSeconds().toString() // 秒
        }
        for (let k in opt) {
          ret = new RegExp('(' + k + ')').exec(fmt)
          if (ret) {
            fmt = fmt.replace(
              ret[1],
              ret[1].length == 1 ? opt[k] : opt[k].padStart(ret[1].length, '0')
            )
          }
        }
        return fmt
      },
      getList() {
        this.listLoading = true
        fetchList(this.listQuery).then(response => {
          this.list = response.data.items
          this.calendarTypeOptions = response.data.calendarTypeOptions
          this.total = response.data.total
          setTimeout(() => {
            this.listLoading = false
          }, 1.5 * 1000)
        })
      },
      handleFilter() {
        this.listQuery.page = 1;
        this.getList()
      },
      handleStag() {
        this.resetTemp();
        this.temp.tempstat = 5
      },
      handleData(paramId,NodeIP) {
        this.handleStag();
        this.temp.id = paramId;
        this.temp.nodeip = NodeIP;
        statustag(this.temp).then(() => {
          this.list.unshift(this.temp);
          this.dialogFormVisible = false;
          this.$notify({
            message: '已经标记为失败',
            type: 'info',
            // duration: 2000
          });
          this.getList();
        })
      },
      // handleModifyStatus(row, status) {
      //   this.$message({
      //     message: '操作成功',
      //     type: 'success'
      //   })
      //   // row.status = status
      // },
      sortChange(data) {
        const { prop, order } = data
        if (prop === 'id') {
          this.sortByID(order)
        }
      },
      sortByID(order) {
        if (order === 'ascending') {
          this.listQuery.sort = '+id'
        } else {
          this.listQuery.sort = '-id'
        }
        this.handleFilter()
      },
      resetTemp() {
        this.temp = {
          id: undefined,
          importance: 1,
          remark: '',
          timestamp: new Date(),
          title: '',
          status: '1',
          type: ''
        }
      },
      handleCreate() {
        this.resetTemp()
        this.dialogStatus = 'create'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      },
      createData() {
        this.fullscreenLoading = true;
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            this.temp.author = this.getCookie();
            console.log(this.temp.author)
            createArticle(this.temp).then(() => {
              // console.log(this.temp)
              this.list.unshift(this.temp)
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              setTimeout(() => {
                this.fullscreenLoading = false
              }, 1.5 * 1000);
              this.getList();
            }).catch(err => {
              console.log(err)
              this.fullscreenLoading = false
            });
          }
        })
      },
      // handleUpdate(row) {
      //   this.temp = Object.assign({}, row) // copy obj
      //   this.temp.timestamp = new Date(this.temp.timestamp)
      //   this.dialogStatus = 'update'
      //   this.dialogFormVisible = true
      //   this.$nextTick(() => {
      //     this.$refs['dataForm'].clearValidate()
      //   })
      // },
      updateData() {
        this.$refs['dataForm'].validate((valid) => {
          if (valid) {
            const tempData = Object.assign({}, this.temp)
            tempData.timestamp = +new Date(tempData.timestamp)
            updateArticle(tempData).then(() => {
              const index = this.list.findIndex(v => v.id === this.temp.id)
              this.list.splice(index, 1, this.temp)
              this.dialogFormVisible = false
              this.$notify({
                title: '成功',
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
            })
          }
        })
      },
      handleDelete(row, index) {
        this.$notify({
          title: '成功',
          message: '删除成功',
          type: 'success',
          duration: 2000
        })
        this.list.splice(index, 1)
      },
      handleFetchPv(pv) {
        fetchPv(pv).then(response => {
          this.pvData = response.data.pvData
          this.dialogPvVisible = true
        })
      },
      handleDownload() {
        this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['timestamp', 'nodeip', 'ipmiadd', 'title', 'versions','author']
          // const filterVal = ['timestamp', 'nodeip', 'ipmiadd', 'title', 'versions','author']
          const filterVal = ['timestamp', 'nodeip', 'ipmiadd', 'title', 'versions','author']
          const data = this.formatJson(filterVal)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'table-list'
          })
          this.downloadLoading = false
        })
      },
      formatJson(filterVal) {
        return this.list.map(v => filterVal.map(j => {
          if (j === 'timestamp') {
            return parseTime(v[j])
          } else {
            return v[j]
          }
        }))
      },
      getSortClass: function(key) {
        const sort = this.listQuery.sort
        return sort === `+${key}` ? 'ascending' : 'descending'
      }
    },
    mounted() {
      this.timer = setInterval(this.getList, 150000);
      // this.timestamp = setInterval(new Date(), 1000);
    },
    beforeDestroy() {
      clearInterval(this.timer);
    }
  }
</script>
