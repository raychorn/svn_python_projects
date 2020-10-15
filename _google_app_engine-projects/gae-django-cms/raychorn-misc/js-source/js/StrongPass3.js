//Strength Password Meter.  By Davide Formica
function StrongPass(fieldvalue) { 
//Initialise variables
fieldlength = fieldvalue.length; 

var meter=0;
	//It must contain at least one number character
	if ((fieldvalue.match(/\d/) )){  
			meter=meter+1;
	}
	//It must contain at least one upper case character     
	if ((fieldvalue.match(/[A-Z]/))) {
			meter=meter+1;
	}
	//It must contain at least one lower case character
	if ((fieldvalue.match(/[a-z]/))) {
			meter=meter+1;
	}
	//It must contain at least one special character
	if ((fieldvalue.match(/\W+/))) {
			meter=meter+1;
	}
	//It must be at least 8 characters long.
	if ((fieldlength >= 8)) {
			meter=meter+1;
	}
	//It must NOT contain a space
	if (fieldvalue.indexOf(" ") > -1) {
		meter=meter-1;
	}     
	//Display meter status and do not allow submit if pass is not at least medium strength
     if (meter == 0){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass0.gif";
	 }
     else if(meter == 1){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass1.gif";
		document.meterlabel_img.src="https://www.openecry.com/Images/x_weak.gif";
		document.Pass1_img.src="https://www.openecry.com/Images/spacer_trans.gif";
		document.Pass2_img.src="https://www.openecry.com/Images/spacer_trans.gif";
	 	return false;
	 }
     else if (meter == 2){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass2.gif";
		document.meterlabel_img.src="https://www.openecry.com/Images/x_weak.gif";
		document.Pass1_img.src="https://www.openecry.com/Images/spacer_trans.gif";
		document.Pass2_img.src="https://www.openecry.com/Images/spacer_trans.gif";
	 	return false;
	 }
     else if (meter == 3){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass3.gif";
		document.meterlabel_img.src="https://www.openecry.com/Images/x_medium.gif";
	 }
     else if (meter == 4){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass4.gif";
		document.meterlabel_img.src="https://www.openecry.com/Images/x_strong.gif";
	 }
     else if (meter == 5){
	 	document.meter_pass.src="https://www.openecry.com/Images/meter_pass5.gif";
	 }
}