<template>
    <div class="query-results">
      <h2>查询结果</h2>
      <div v-for="(result, index) in results" :key="index" class="result-item">
        <h3>{{ result.title }}</h3>
        <p>{{ result.description }}</p>
        <table>
          <thead>
            <tr>
              <th v-for="header in result.headers" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in result.data" :key="row.id">
              <td v-for="cell in row" :key="cell">{{ cell }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      results: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .query-results {
    margin: 20px;
  }
  .result-item {
    margin-bottom: 20px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  </style>