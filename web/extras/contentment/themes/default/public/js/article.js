$(function(){
    $('.modify-link').click(function(){
        $('.indent').load(articlePath + "/editable", function(){
            $('.modify-link').addClass('selected');
            $('textarea').focus();
            $('.modify').submit(function(){
                var localTime = new Date();
                var data = new Object();
                
                $('form.modify input[type=text], form.modify textarea, form.modify select').each(function(index, element){
                    data[$(element).attr('name')] = $(element).val();
                });
                
                $('.indent').load(articlePath + "?v=" + localTime.getTime(), data, function(){ $('.modify-link').removeClass('selected'); });
                return false;
            });
        });
        return false;
    });

    $('.delete-link').click(function(){ return confirm('Are you sure you wish to delete this article?  This action can not be un-done.'); });
});