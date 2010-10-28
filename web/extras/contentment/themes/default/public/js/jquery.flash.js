/*

Life as Me: Flash Message jQuery Plugin
Copyright (c) 2008 Alice Bevan-McGregor. All Rights Reserved.

Permission is granted to use and modify this file as long as this original header remains intact.

Changelog:

    1.0     Initial release.
    1.1     Updated to use setTimeout vs. the elem.animate() hack.
    
*/

jQuery.Flash = function(element){
    this.element = $(element);
    this.timeout = undefined;
    
    var content = $('<div><label></label><span></span></div>')
    
    this.element.hide()
        .click(function(){ jQuery.flash.hide(); })
        .hover(function(){ jQuery.flash.onOver(); }, function(){ jQuery.flash.onLeave(); })
        .append(content);
};

jQuery.Flash.version = 1.1;

jQuery.Flash.prototype.onOver = function() {
    this.element.addClass('over');
}

jQuery.Flash.prototype.onLeave = function() {
    this.element.removeClass('over');
    
    if ( this.element.hasClass('expired') ) this.hide();
}

jQuery.Flash.prototype.onTimeout = function() {
    this.element.addClass('expired');
    if ( ! this.element.hasClass('over') ) this.hide();
}

jQuery.Flash.prototype.show = function() {
    this.element.fadeIn(1000);
    
    if ( ! this.element.hasClass('error') )
        this.timeout = window.setTimeout(function(){ jQuery.flash.onTimeout() }, 15000);
}

jQuery.Flash.prototype.hide = function() {
    if ( this.timeout ) {
        clearTimeout(this.timeout);
        this.timeout = undefined;
    }
    
    this.element.fadeOut(1000).removeClass('expired').removeClass('over');
}

jQuery.Flash.prototype.message = function(klass, label, message) {
    this.element.removeClass('expired');
    
    if ( this.element.is(":visible") ) {
        if ( this.timeout ) {
            clearTimeout(this.timeout);
            this.timeout = undefined;
        }
        
        this.element.fadeOut(1000, function(){ jQuery.flash.message(klass, label, message); });
        return;
    }
    
    this.element.attr('class', klass);
    this.element.find('label').text(label);
    this.element.find('span').text(message);
    
    this.show();
}

jQuery.Flash.prototype.subtle = function(label, message) { this.message('subtle', label, message); }
jQuery.Flash.prototype.error = function(label, message) { this.message('error', label, message); }
jQuery.Flash.prototype.failure = function(label, message) { this.message('failure', label, message); }
jQuery.Flash.prototype.fail = function(label, message) { this.message('failure', label, message); }
jQuery.Flash.prototype.warning = function(label, message) { this.message('warning', label, message); }
jQuery.Flash.prototype.warn = function(label, message) { this.message('warning', label, message); }
jQuery.Flash.prototype.information = function(label, message) { this.message('information', label, message); }
jQuery.Flash.prototype.info = function(label, message) { this.message('information', label, message); }
jQuery.Flash.prototype.success = function(label, message) { this.message('success', label, message); }

$(function(){
    jQuery.flash = new jQuery.Flash('#flash');
    
    $('#message').each(function(index, element){
        var elem = $(element);
        jQuery.flash.message(elem.attr('class'), elem.attr('title'), elem.html());
    });
});