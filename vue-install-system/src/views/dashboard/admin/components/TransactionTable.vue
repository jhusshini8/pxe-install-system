<template>
  <el-table :data="list" style="width: 100%;padding-top: 15px;">
    <el-table-column label="系统" min-width="200">
      <template slot-scope="scope">
        <!--{{ scope.row.order_no | orderNoFilter }}-->
        {{ scope.row.installsystem }}
      </template>
    </el-table-column>
    <el-table-column label="用户" width="195" align="center">
      <template slot-scope="scope">
        <!--¥{{ scope.row.price | toThousandFilter }}-->
        {{ scope.row.name }}
      </template>
    </el-table-column>
    <el-table-column label="状态" width="100" align="center">
      <template slot-scope="{row}">
        <el-tag :type="row.status | statusFilter">
          {{ row.status }}
        </el-tag>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { transactionList } from '@/api/remote-search'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        '成功': 'success',
        '失败': 'danger',
        "安装中": 'warning'
      }
      return statusMap[status]
    },
    orderNoFilter(str) {
      return str.substring(0, 30)
    }
  },
  data() {
    return {
      list: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      transactionList().then(response => {
        this.list = response.data.items.slice(0, 8)
      })
    }
  }
}
</script>
