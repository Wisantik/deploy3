import React from "react";
import Dialogs from "./Dialogs";
import { connect } from "react-redux";
import { createMessage, setId } from "../../redux/reducers/MessageReducer";
import { deleteDialog } from "../../redux/reducers/DIalogsReducer";
const DialogsContainer = (props) => {
    return(
        <Dialogs setId = {props.setId} item = {props.item} deleteDialog = {props.deleteDialog} />
    )
}
const mapStateToProps = (state) => ({

})
export default connect(mapStateToProps,{setId,deleteDialog})(DialogsContainer)