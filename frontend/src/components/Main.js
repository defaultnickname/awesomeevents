import React, { Component, useEffect } from "react";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormControl from "@material-ui/core/FormControl";
import Button from "@material-ui/core/Button";
import { authenticationService } from "../services/authenticationservice";
import {reservationService} from "../services/reservationService";
import ReservationItem from "./ReservationItem";
import NavBar from "./NavBar";

export default class Main extends Component {
  constructor(props) {
    super(props);

    this.state = {
      currentUser: authenticationService.currentUserValue,
      reservations: undefined,
      isLoaded: false,
    };
  }

  componentDidMount() {
    authenticationService.currentUser.subscribe((x) =>
      this.setState({ currentUser: x })
    );
    this.getReservations();
  }


  getReservations() {
    reservationService.getEvents()
      .then((resp) => resp.json())
      .then((reservations) => {
        console.log(reservations,"reservations")
        this.setState({
          reservations: reservations,
          isLoaded: true,
        });
      });
  }

  render() {
    const { currentUser, reservations, isLoaded } = this.state;

  }
}
