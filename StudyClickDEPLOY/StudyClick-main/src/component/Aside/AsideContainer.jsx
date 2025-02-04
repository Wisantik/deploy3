import React from "react";
import Aside from "./Aside";
import { connect } from "react-redux";
import { AddDialogs } from "../../redux/reducers/DIalogsReducer";
const AsideContainer = (props) => {
    return(
    <Aside  dialogs = {props.dialogs} AddDialogs = {props.AddDialogs} dialogs_history = {props.dialogs_history} />
    )
}
const mapStateToProps = (state) => ({
    dialogs: state.dialogs.dialogs_data,
})
export default connect(mapStateToProps,{AddDialogs,})(AsideContainer)