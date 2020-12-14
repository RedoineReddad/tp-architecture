<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Tickets</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Departure airport</th>
              <th scope="col">Departure Time</th>
              <th scope="col">Arrival airport</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(ticket, index) in tickets" :key="index">
              <td>{{ ticket.dep_code }}</td>
              <td>{{ ticket.dep_time }}</td>
              <td>{{ ticket.arr_code }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tickets: [],
    };
  },
  methods: {
    getTickets() {
      const path = 'http://localhost:5000/tickets/available';
      axios.get(path)
        .then((res) => {
          this.tickets = res.data.tickets;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getTickets();
  },
};
</script>
