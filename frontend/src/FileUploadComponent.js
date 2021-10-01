import React, { Component } from 'react';
import axios from 'axios';

export default class FileUploadComponent extends Component {

    constructor(props) {
        super(props);

        this.onFileChange = this.onFileChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);

        this.state = {
            foodImg: ''
        }
    }

    onFileChange(e) {
        this.setState({ foodImg: e.target.files[0] })
    }

    onSubmit(e) {
        e.preventDefault()
        const formData = new FormData()
        formData.append('foodImg', this.state.foodImg)
        axios.post("/api/image-upload-test", formData, {
        }).then(res => {
            console.log(res)
        }).catch(err => {
            console.log(err)
        })
    }


    render() {
        return (
            <div className="container">
                <div className="row">
                    <form onSubmit={this.onSubmit}>
                        <div className="form-group">
                            <input type="file" onChange={this.onFileChange} />
                        </div>
                        <div className="form-group">
                            <button className="btn btn-primary" type="submit">Upload</button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}