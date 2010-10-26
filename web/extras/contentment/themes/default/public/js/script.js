$(function(){
    $.plugins({
            plugins: [
                    {
                        id: 'timeago',
                        js: ['/theme/static/js/jquery.timeago.js'],
                        fn: ['timeago'],
                        ext: ['timeago'],
                        sel: 'time'
                    },
                    {
                        id: 'tabify',
                        js: ['/theme/static/js/jquery.tabify-1.4.js'],
                        fn: ['tabify'],
                        sel: 'menu.tabs'
                    }
                    // {
                    //     id: 'upload',
                    //     js: ['/static/js/jquery.html5upload.js'],
                    //     fn: ['html5_upload'],
                    //     sel: 'input[multiple=multiple]'
                    // },
                ]
        });
    
    $("a[href$='/action:delete']").click(function(){ return confirm("Are you sure you wish to delete this resource?\n\nThis can not be undone, and will delete any child resources contained within."); });
});