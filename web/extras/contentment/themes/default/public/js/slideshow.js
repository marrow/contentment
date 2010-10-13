// Simmple custom slideshow class for getmvp.com homepage


function SlideShow() {
	this.current_slide = 1;
	this.total_slides = 1;
	this.slide_title_id = "slide-title";
	this.slide_description_id = "slide-description";
	this.slide_image_id = "slide-image";
        this.lightbox_link_id = "lightbox-link";
	
	this.radio_on_img_src = "images/design/slide-radio-on.gif";
	this.radio_off_img_src = "images/design/slide-radio-off.gif";
	this.radio_id_prefix = "radio-";
	this.slide_data = [];
}

SlideShow.prototype.setSlideData = function( data_array ) {
	this.slide_data = data_array;
	this.total_slides = slide_data.length - 1;
}

SlideShow.prototype.setTotalSlides = function( num ) {
	this.total_slides = num;
}

SlideShow.prototype.nextSlide = function() {
  //    window.blur();
    if( this.current_slide != this.total_slides ) {
        this.switchSlide( this.current_slide + 1 );
    }	
}

SlideShow.prototype.previousSlide = function() {
  //	window.blur();
    if( this.current_slide != 1 ) {
        this.switchSlide( this.current_slide - 1 );
    }
}

SlideShow.prototype.switchSlide = function( slide_num ) {
  //	window.blur();

    var slide_id = parseInt( slide_num );
    var data = this.slide_data[slide_id];

    // if they havent clicked the currently active radio button
    if( slide_id != this.current_slide) {

        // turn the clicked radio button image to on
        var off_radio_id_ref = this.radio_id_prefix + slide_id;
        var off_radio_img_tag = document.getElementById( off_radio_id_ref );
            off_radio_img_tag.src = this.radio_on_img_src;

        // turn the currently active radio button image off
        var on_radio_id_ref = this.radio_id_prefix + this.current_slide;
        var on_radio_img_tag = document.getElementById( on_radio_id_ref );
            on_radio_img_tag.src = this.radio_off_img_src;

        // change the title
        var titleTag = document.getElementById( this.slide_title_id );
            titleTag.lastChild.nodeValue = this.slide_data[ slide_id ].title;

        // change the description
        var descTag = document.getElementById( this.slide_description_id );
            descTag.lastChild.nodeValue = this.slide_data[ slide_id].description;

        // change the screen image source
	//	var slide_img_tag = document.getElementById( this.slide_image_id );
        //	slide_img_tag.src = this.slide_data[slide_id].image;

        // change the screen image source
		var slide_img_tag = document.getElementById( this.slide_image_id );
        	slide_img_tag.src = data.image.src;

	// change the screen image lightbox link
	var lightbox_link = document.getElementById( this.lightbox_link_id );
	    lightbox_link.href = data.image.link;
	    lightbox_link.title = data.image.title;


        this.current_slide = slide_id;
    }
}
