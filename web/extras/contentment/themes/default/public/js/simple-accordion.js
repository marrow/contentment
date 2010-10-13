// Create an instanceof a simple accordion and use the instance to pass in an id reference to show
// Keeps track of the previous id reference so that it can hide it.
// Usage:
// var acc = new SimpleAccordion();
//     acc.showAccordionPanel('idReferenceToHiddenPanel'); return false;
// ------------------------------------------------------------------------------------------------

function SimpleAccordion() {
	this.current_panel = "";
}

SimpleAccordion.prototype.showAccordionPanel = function( idRef ) {
	// If the user hasn't clicked to open the currently active panel
    
	window.blur();

	if( this.current_panel != idRef ) {

        // Get the panel and show it
        var panel_to_show = document.getElementById( idRef );
	        panel_to_show.style.display = "block";  

	    // Only hide the panel if a current_panel has been set to avoid errors
	    if( this.current_panel != "" ) {
	        var panel_to_hide = document.getElementById( this.current_panel );
    	        panel_to_hide.style.display = "none";
	    }
	
		// Set our current_panel to the new panel passed in
	    this.current_panel = idRef;
    }
	// If the user clicks the currently active panel - lets close it.
	else if( this.current_panel == idRef ) {
		var panel_to_hide = document.getElementById( this.current_panel );
			panel_to_hide.style.display = "none";
			
		// Set current_panel to nil - nothing is activated at this time
		this.current_panel = "";
	}
}
