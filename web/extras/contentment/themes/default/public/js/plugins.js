(function($){var plugins={};var loaded={};var loader=function(files,force,call){if($.isArray(files)&&files.length>0){var file=files.shift();$.include(file,(force)?true:function(){loader(files,call);});}else{if($.isFunction(call))call($);}};var load=function(plugin,arg){var force=false;var call=function(){return true;};if(arg){if($.isFunction(arg))call=arg;else force=true;}
if(!plugin)throw'Invalid plugin call';call=$.isFunction(call)?call:function(){return true;};if(plugin.loaded)return call($);if(plugin.loading)return setTimeout(function(){load(plugin,call);},5);plugin.loading=true;var files=$.makeArray(plugin.css);files=files.concat($.makeArray(plugin.js));loader(files,force,function(){plugin.loaded=true;call($);});};var extend=function(arr,scope,plugin){$.each($.makeArray(arr),function(){var name=this;if(typeof(scope[name])=='undefined'){scope[name]=function(){var self=this;var args=arguments;load(plugin,function(){scope[name].apply(self,args);});};}});};var createEl=function(type,attr){var el=document.createElement(type);$.each(attr,function(key){if(typeof(attr[key])!='undefined')el.setAttribute(key,attr[key]);});return el;};$.included=function(file){if(typeof(loaded[file])!='undefined')return true;return loaded[file]=($((/.css$/.test(file)?'link[href':'script[src')+'*="'+file+'"]').length>0);};$.include=function(file,arg){var force=false;var call=function(){};if(arg){if($.isFunction(arg))call=arg;else force=true;}
if($.included(file)){if(/-ie.$/.test(file)&&!$.browser.msie)return call();else if(/-saf.$/.test(file)&&!$.browser.safari)return call();else if(/-opera.$/.test(file)&&!$.browser.opera)return call();else if(/-moz.$/.test(file)&&!$.browser.mozilla)return call();else call();}
var el;var css=/.css$/.test(file);if(css){if(force){$('body').append('<link type="text/css" rel="stylesheet" href="'+file+'" />');}else{el=createEl('link',{'type':'text/css','rel':'stylesheet','href':file});if($.browser.msie)el.onreadystatechange=function(){/loaded|complete/.test(el.readyState)&&call();};else if($.browser.opera)el.onload=call;else{(function(){try{el.sheet.cssRule;}catch(e){setTimeout(arguments.callee,20);return;};call();})();}
$('head').get(0).appendChild(el);}}else{if(force){$('body').append('<scr'+'ipt type="text/javascript" src="'+file+'"></scr'+'ipt>');}else{el=createEl('script',{'type':'text/javascript','src':file});if($.browser.msie)el.onreadystatechange=function(){/loaded|complete/.test(el.readyState)&&call();};else el.onload=call;$('head').get(0).appendChild(el);}}};$.plugin=function(plugin){if(plugin.id){plugin.loaded=false;if(typeof(plugins[plugin.id])=='undefined'){plugins[plugin.id]=plugin;extend(plugin.ext,$,plugin);extend(plugin.fn,$.fn,plugin);plugin.sel=$.makeArray(plugin.sel);$(document).ready(function(){for(var i=0;i<plugin.sel.length;i++)if($(plugin.sel[i]).length>0){load(plugin);break;}});}}};$.plugins=function(options){var path=options.path||'';options=options.plugins||options||[];$.each(options,function(){var plugin=this;plugin.css=$.makeArray(plugin.css);for(var i=0;i<plugin.css.length;i++)plugin.css[i]=path+plugin.css[i];plugin.js=$.makeArray(plugin.js);for(var i=0;i<plugin.js.length;i++)plugin.js[i]=path+plugin.js[i];$.plugin(plugin);});};$.requires=function(id,call){var plugin=plugins[id];if(typeof(plugin)!='undefined')load(plugin,call);else throw'$.requires could not find ['+id+']';};})(jQuery);window.log=function(){log.history=log.history||[];log.history.push(arguments);if(this.console){console.log(Array.prototype.slice.call(arguments));}};(function(){var docwrite=document.write;document.write=function(q){log('document.write(): ',q);if(/docwriteregexwhitelist/.test(q))docwrite(q);}})();