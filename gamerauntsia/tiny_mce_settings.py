TINYMCE_DEFAULT_CONFIG = {
    "language": 'eu',
    "themes": "modern",
    "height": 600,
    "plugins": [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste",
    ],
    "toolbar": "styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview",
    "menubar": False,
    "media_alt_source": False,
    "media_poster": False,
    "media_dimensions": False,
    "extended_valid_elements" : "script[src|type|language]",
    "relative_urls": False,
    "remove_script_host": True
}

TINYMCE_SMALL_BODY_CONFIG = {
    "language": 'eu',
    "themes": "modern",
    "plugins": [
        "advlist autolink lists link image charmap print preview anchor",
        "searchreplace visualblocks code fullscreen",
        "insertdatetime media table contextmenu paste",
    ],
    "toolbar": "styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | preview",
    "theme_advanced_resizing": True,
    "relative_urls": False,
    "remove_script_host": True
}
