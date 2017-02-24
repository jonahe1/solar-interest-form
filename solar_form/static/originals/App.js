import React, { Component } from 'react';

class InterestForm extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         name: "",
         age: 0,
         address: "",
         city: "",
         state: "",
         zip: "",
         interest: "",
         message: "",
         submitFailed: false
      };

      this.handleInputChange = this.handleInputChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.submitData = this.submitData.bind(this);
      this.inputBox = this.inputBox.bind(this);
      this.dropdownBox = this.dropdownBox.bind(this);
   }

   handleInputChange(event) {
      const target = event.target;
      const value = target.value;
      const name = target.name;
      this.setState({
         [name]: value
      });
   }

   handleSubmit(event) {
      for (var key in this.state) {
         if (!this.state[key]) {
            this.setState({
               message: "Form incomplete",
               submitFailed: true
            });
            event.preventDefault();
            return;
         }
      }
      this.setState({
         name: "",
         age: 0,
         address: "",
         city: "",
         state: "",
         zip: "",
         interest: "",
         message: "Your response has been recorded. Thanks for submitting!",
         submitFailed: false,
      });
      event.preventDefault();
      this.submitData();
   }

   submitData() {
      const formData = new FormData();
      formData.append('name', this.state.name);
      formData.append('age', this.state.age);
      formData.append('address', this.state.address);
      formData.append('city', this.state.city);
      formData.append('state', this.state.state);
      formData.append('zip', this.state.zip);
      formData.append('interest', this.state.interest);

      let data = {
         method: 'post',
         body: formData
      }
      try {
         return fetch('http://127.0.0.1:5000/', data)
      } catch(error) {
         console.error(error);
      }
   }

   inputBox(type) {
      var inputStyle = {
         padding: 5,
         display: "block",
         width: 375,
         borderRadius: 7,
         border: "2px solid #dadada",
         borderColor: "",
      };
      if (!this.state[type] && this.state.submitFailed) {
         inputStyle.borderColor = "#ff0000";
      } else {
         inputStyle.borderColor = "#9ecaed";
      }
      return (
         <input style={inputStyle}
         name={type}
         type="text"
         value={this.state[type]}
         onChange={this.handleInputChange} />
      );
   }

   textAreaBox() {
      var textAreaStyle = {
         height: 50,
         width: 387,
         paddingBottom: 0.4,
         paddingRight: 0.4,
         borderRadius: 7,
         border: "2px solid #dadada",
         borderColor: "",
      };
      if (!this.state.interest && this.state.submitFailed) {
         textAreaStyle.borderColor = "#ff0000";
      } else {
         textAreaStyle.borderColor = "#9ecaed";
      }
      return (
         <textarea style={textAreaStyle}
         name="interest"
         type="text"
         value={this.state.interest} onChange={this.handleInputChange} />
      );
   }

   dropdownBox() {
      var dropDownStyle = {
         display: "block",
         borderRadius: 7,
         border: "2px solid #dadada",
         borderColor: "",
      };
      if (!this.state.state && this.state.submitFailed) {
         dropDownStyle.borderColor = "#ff0000";
      } else {
         dropDownStyle.borderColor = "#9ecaed";
      }
      return (
         <select value={this.state.state} onChange={this.handleInputChange} name='state' style={dropDownStyle}>
         <option value="">--Select--</option>
         <option value="AL">Alabama</option>
         <option value="AK">Alaska</option>
         <option value="AZ">Arizona</option>
         <option value="AR">Arkansas</option>
         <option value="CA">California</option>
         <option value="CO">Colorado</option>
         <option value="CT">Connecticut</option>
         <option value="DE">Delaware</option>
         <option value="DC">District Of Columbia</option>
         <option value="FL">Florida</option>
         <option value="GA">Georgia</option>
         <option value="HI">Hawaii</option>
         <option value="ID">Idaho</option>
         <option value="IL">Illinois</option>
         <option value="IN">Indiana</option>
         <option value="IA">Iowa</option>
         <option value="KS">Kansas</option>
         <option value="KY">Kentucky</option>
         <option value="LA">Louisiana</option>
         <option value="ME">Maine</option>
         <option value="MD">Maryland</option>
         <option value="MA">Massachusetts</option>
         <option value="MI">Michigan</option>
         <option value="MN">Minnesota</option>
         <option value="MS">Mississippi</option>
         <option value="MO">Missouri</option>
         <option value="MT">Montana</option>
         <option value="NE">Nebraska</option>
         <option value="NV">Nevada</option>
         <option value="NH">New Hampshire</option>
         <option value="NJ">New Jersey</option>
         <option value="NM">New Mexico</option>
         <option value="NY">New York</option>
         <option value="NC">North Carolina</option>
         <option value="ND">North Dakota</option>
         <option value="OH">Ohio</option>
         <option value="OK">Oklahoma</option>
         <option value="OR">Oregon</option>
         <option value="PA">Pennsylvania</option>
         <option value="RI">Rhode Island</option>
         <option value="SC">South Carolina</option>
         <option value="SD">South Dakota</option>
         <option value="TN">Tennessee</option>
         <option value="TX">Texas</option>
         <option value="UT">Utah</option>
         <option value="VT">Vermont</option>
         <option value="VA">Virginia</option>
         <option value="WA">Washington</option>
         <option value="WV">West Virginia</option>
         <option value="WI">Wisconsin</option>
         <option value="WY">Wyoming</option>
         </select>
      );
   }

   render() {
      var alertStyle = {
         color: "#00F",
         marginLeft: 50,
         margin: 5,
         backgroundColor: "#66CCCC",
         borderRadius: 15,
         textAlign: "center"
      };
      if (this.state.message) {
         var status = <div id="status" className='alert' style={alertStyle} ref="status">
         {this.state.message}
         </div>;
      }
      var labelStyle = {
         marginLeft: 25,
         marginTop: 20,
         width: 400,
         color: "#ffffff",
         display: "inline-block",
         fontStyle: "italic"
      };
      var formStyle = {
         marginLeft: "auto",
         marginRight: "auto",
         width: 450,
         position: "relative",
         fontFamily: "Verdana, Geneva, sans-serif",
         fontSize: "18",
         backgroundColor: "#303030",
         borderRadius: 15
      };
      var titleStyle = {
         marginLeft: 20,
         marginTop: 20,
         marginBottom: 5,
         fontWeight: "bold",
         color: "#ffffff"
      };
      var buttonStyle = {
         width: 425,
         marginLeft: 10,
         marginBottom: 10
      };
      return (
         <form onSubmit={this.handleSubmit} style={formStyle}>
         <h1 style={titleStyle}>Solar Panel Interest </h1>
         {status}
         <label style={labelStyle}>
         Full Name:
         {this.inputBox("name")}
         </label>
         <br />
         <label style={labelStyle}>
         Age:
         {this.inputBox("age")}
         </label>
         <br />
         <label style={labelStyle}>
         Street Address:
         {this.inputBox("address")}
         </label>
         <br />
         <label style={labelStyle}>
         City:
         {this.inputBox("city")}
         </label>
         <br />
         <label style={labelStyle}>
         State:
         {this.dropdownBox()}
         </label>
         <br />
         <label style={labelStyle}>
         Zipcode:
         {this.inputBox("zip")}
         </label>
         <br />
         <label style={labelStyle}>
         What's your interest in Solar Panels?
         <br />
         {this.textAreaBox()}
         </label>
         <br />
         <input style={buttonStyle} type="submit" value="Submit Form" />
         </form>
      );
   }
}

export default InterestForm;
