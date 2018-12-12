{% set prototypes_list_of_routes = ['/prototypes','/mybank','/mygame'] %}
{% set about_list_of_routes = ['/about','/contact','/terms_and_conditions','/privacy_policy','/cookies_policy'] %}
{% set home_is_active='' %}
{% set company_is_active='' %}
{% set why_is_active='' %}
{% set research_is_active='' %}
{% set academy_is_active='' %}
{% set knowledge_is_active='' %}
{% set services_is_active='' %}
{% set prototypes_is_active='' %}
{% set about_is_active='' %}

{% if request.path == '/' or request.path == '/home' %}
    {% set home_is_active='active' %}
{% endif %}
{% if request.path == '/company' %}
    {% set company_is_active='active' %}
{% endif %}
{% if request.path == '/why' %}
    {% set why_is_active='active' %}
{% endif %}
{% if request.path == '/research' %}
    {% set research_is_active='active' %}
{% endif %}
{% if request.path == '/academy' %}
    {% set academy_is_active='active' %}
{% endif %}
{% if request.path == '/knowledge' %}
    {% set knowledge_is_active='active' %}
{% endif %}
{% if request.path == '/services' %}
    {% set services_is_active='active' %}
{% endif %}
{% if request.path in  prototypes_list_of_routes %}
    {% set prototypes_is_active='active' %}
{% endif %}
{% if request.path in  about_list_of_routes %}
    {% set about_is_active='active' %}
{% endif %}


{% set help_list_of_routes=['/prototypes','/mybank','/mygame'] %}
{% set login_active='' %}
{% set register_active='' %}
{% set help_active='' %}
{% if request.path == '/login' %}
    {% set login_active='active' %}
{% endif %}
{% if request.path == '/register' %}
    {% set register_active='active' %}
{% endif %}
{% if request.path in  help_list_of_routes %}
    {% set help_active='active' %}
{% endif %}


<nav class="navbar navbar-expand-md bg-light navbar-light w-100" style="padding-top:0px;padding-bottom:0px">
    <div class="row">
        <!-- brand and logo -->
        <div class="page_title border border-warning">
            <span class="xnavbar-brand">
                <a href="/" class="xnavbar-brand"><img id="logo" src="../../static/images/ganimides_logoB3.gif" alt="{{COMPANY_NAME}}" /></a>
            </span>
            <span class="page_title">
            {{WEBSITE_TITLE}}
            </span>
        </div>
        <!-- Toggler/collapsibe Button -->
        <div class="border border-danger">
            <button class="navbar-toggler ml-auto xcustom-toggler" type="button" data-toggle="collapse" data-target="#GlobalMenu" aria-controls="GlobalMenu" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
        <!--/////////////////////////////////////-->
        <div class="border border-info justify-content-end">
            <!-- SUPPORT MENU  -->
            <div id="SupportMenu" class="collapse navbar-collapse xborder xborder-danger support_menu_navbar">
                <ul class="navbar-nav ml-auto font-weight-light">
                    <li class="nav-item dropdown">
                        <a id="searchform" data-toggle="tooltip" title="search" data-placement="bottom" class="nav-link" href="javascript:function(){document.getElementById('top-menu-search').show();}"><img class="menu_image" src="../../static/images/icon_search.gif" alt="search" onmouseover="this.src = '../../static/images/icon_search_green.gif';" onmouseout="this.src = '../../static/images/icon_search.gif';" /></a>
                        <div class="dropdown-menu" aria-labelledby="searchform">
                            <form class="form-inline mt-2 mt-md-0 top-menu-navbar-search-form">
                                <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
                                <button type="submit" class="btn btn-info btn-sm">Search</button>
                            </form>
                        </div>
                    </li>
                    {% if not(current_user.is_authenticated) %}
                        <li class="{{login_active}} nav-item">
                            <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.login_or_register',action_tab='login')}}">Log-in</a>
                        </li>

                        <li class="{{register_active}} nav-item">
                            <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.login_or_register',action_tab='register')}}}">Register</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.logout')}}">Logout</a>
                        </li>
                    {% endif %}

                    <li class="{{help_active}} nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="{{url_for('prototypes')}}" id="ProtoTypesDropdownList" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">Help&nbsp;</a>
                        <div class="dropdown-menu dropdown_list" aria-labelledby="helpDropdownList">
                            <a class="dropdown-item" href="/myBank">MyBank</a>
                            <a class="dropdown-item" href="{{url_for('home.myGame')}}">MyGame</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{{ url_for('home.sendtestemail') }}">send test email</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-carousel-5-single-multiple-horizontal-and-vertical-sliding-demos/">Carousel</a>
                            <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-form-customized-styles-6-online-examples/">Forms</a>
                            <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-select-5-beautiful-styles/">beautifull styles</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="https://www.rocketlawyer.co.uk/">Rocket Lawyer</a>
                            <a class="dropdown-item" href="https://www.w3schools.com/bootstrap4/bootstrap_navbar.asp">bootstrap4</a>
                            <a class="dropdown-item" href="https://summerofcode.withgoogle.com/?csw=1">Summer Code Project</a>
                            <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                            <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                            <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                            <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-select-5-beautiful-styles/">Select</a>
                        </div>
                    </li>
                    <li class="nav-item dropdown">
                        <!--show the active language-->
                        {% for language in AVAILABLE_LANGUAGES.items() %}
                            {% if CURRENT_LANGUAGE == language[0] %}
                                {% set language_picture=flag_file(language[1][1]) %}
                                <a class="nav-link dropdown-toggle" href="#" id="languageDropdownList" role="button" data-toggle="dropdown" aria-expanded="false">
                                    <img class="menu_image" src="{{language_picture}}" alt="{{language[1][1]}}" />&nbsp;{{language[1][0]}}
                                </a>
                            {%  endif %}
                        {% endfor %}
                        <!--show the other languages as menu-->
                        <div class="dropdown-menu dropdown_list" aria-labelledby="languageDropdownList">
                            {% for language in AVAILABLE_LANGUAGES.items() %}
                                {% if CURRENT_LANGUAGE != language[0] %}
                                    {% set language_picture=flag_file(language[1][1]) %}
                                    <a class="dropdown-item" href="{{ url_for('set_language', language=language[0]) }}">
                                        <img class="menu_image" src="{{language_picture}}" alt="{{language[1][1]}}" />&nbsp;{{language[1][0]}}
                                    </a>
                                {%  endif %}
                            {% endfor %}
                        </div>
                    </li>
                    <li class="nav-item dropdown">
                    {% if current_user.is_authenticated %}
                        <a class="nav-link dropdown-toggle" href="#" id="usermenu1" role="button" data-toggle="dropdown" aria-expanded="false">
                            {% if current_user.avatarImageFile %}
                                {% set avatarImageFile=current_user.avatarImageFile %}
                            {% else %}
                                {% set avatarImageFile=image_file('icon_avatar_default.png') %}
                            {% endif %}
                            <img class="menu_image rounded-circle border border-dark" alt="" src='{{avatarImageFile}}'>
                        </a>
                        <div class="dropdown-menu dropdown_list" aria-labelledby="usermenu1">
                            <a class="dropdown-item" href="#">Signed-in as {{ current_user.firstName.lower() }}</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{{ url_for('home.logout') }}">Logout</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{{ url_for('home.userprofile') }}">Your Profile</a>
                            <a class="dropdown-item" href="{{ url_for('home.userprofilechange') }}">Change Profile</a>
                            <a class="dropdown-item" href="{{ url_for('home.passwordchange') }}">Change Password</a>
                            <a class="dropdown-item" href="{{ url_for('home.upload_avatar') }}">Change Your Avatar</a>
                            <div class="dropdown-divider"></div>
                            {% if not(current_user.mobileConfirmed) and current_user.mobile %}
                                <a class="dropdown-item" href="{{ url_for('home.mobileconfirm') }}">Confirm Your Mobile</a>
                            {% endif %}
                            {% if not(current_user.emailConfirmed) %}
                                <a class="dropdown-item" href="{{ url_for('home.emailconfirmrequest') }}">Confirm Your Email</a>
                            {% endif %}
                            <div class="dropdown-divider"></div>
                            {% if current_user.passwordreset %}
                                <a class="dropdown-item" href="{{ url_for('home.password_reset',email='*') }}">Reset Your Password</a>
                            {% else %}
                                <a class="dropdown-item" href="{{ url_for('home.forgetpassword') }}">Reset Your Password</a>
                            {% endif %}
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Setting</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="#">Help</a>
                        </div>
                    {% else %}
                        <!--
                        <a class="nav-link dropdown-toggle" href="#" id="usermenu2" role="button" data-toggle="dropdown" aria-expanded="false">
                            <img class="menu_image rounded-circle" alt="" src="../../static/images/icon_user_not_loggedIn.png">
                        </a>
                        <div class="dropdown-menu dropdown_list" aria-labelledby="usermenu2">
                            <a class="dropdown-item" href="{x url_for('home.login') }}"><span class="glyphicon glyphicon-log-in"></span> Login</a>
                            <a class="dropdown-item" href="{x url_for('home.register') }}"><span class="glyphicon glyphicon-user"></span> Register</a>
                        </div>
                        -->
                    {% endif %}
                    </li>
                </ul>
            </div>
        </div>
    </div>
    <div class="row">
        <!--/////////////////////////////////////-->
        <!-- MAIN MENU collapsibleNavbar -->
        <div id="GlobalMenu" class="collapse navbar-collapse border border-primary global_menu_navbar">
            <ul class="navbar-nav">
                <li class="home_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('homepage')}}">Home</a></li>
                <li class="company_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('company')}}">Company</a></li>
                <li class="why_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('why')}}">Why Ganimides</a></li>
                <li class="research_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('research')}}">Research</a></li>
                <li class="academy_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('academy')}}">FinTec Academy</a></li>
                <li class="knowledge_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('knowledge')}}">knowledge center</a></li>
                <li class="services_is_active nav-item"><a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('services')}}">Services</a></li>
                <li class="prototypes_is_active nav-item dropdown"><a title="our prototypes" class="nav-link dropdown-toggle" href="{{url_for('prototypes')}}" id="ProtoTypesDropdownList" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">Prototypes&nbsp;</a>
                    <div class="dropdown-menu dropdown_list" aria-labelledby="ProtoTypesDropdownList">
                        <a class="dropdown-item" href="/myBank">MyBank</a>
                        <a class="dropdown-item" href="{{url_for('home.myGame')}}">MyGame</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-carousel-5-single-multiple-horizontal-and-vertical-sliding-demos/">Carousel</a>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-form-customized-styles-6-online-examples/">Forms</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="{{url_for('research')}}">Research</a>
                        <a class="dropdown-item" href="{{url_for('academy')}}">FinTec Academy</a>
                        <a class="dropdown-item" href="{{url_for('services')}}">Services</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-select-5-beautiful-styles/">Select</a>
                    </div>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li class="about_is_active nav-item dropdown"><a class="nav-link dropdown-toggle" href="#" id="AboutDropdownList" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">About&nbsp;</a>
                    <div class="dropdown-menu  dropdown_list" aria-labelledby="AboutDropdownList">
                        <a class="dropdown-item" href="{{url_for('about')}}">About Us</a>
                        <a class="dropdown-item" href="{{url_for('contact')}}">Contact</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="{{url_for('terms_and_conditions')}}">Terms &amp; Conditions of use</a>
                        <a class="dropdown-item" href="{{url_for('privacy_policy')}}">Privacy Policy</a>
                        <a class="dropdown-item" href="{{url_for('cookies_policy')}}">Cookies Policy</a>
                        <div class="dropdown-divider"></div>
                    </div>
                </li>
            </ul>
            <!--------only on small screens--------------------->
            <ul class="navbar-nav collapse.show sr-only ml-auto hidden-sm-up">
                <li class="nav-item dropdown hidden-sm-up">
                    <a id="searchform" data-toggle="tooltip" title="search" data-placement="bottom" class="nav-link" href="javascript:function(){document.getElementById('top-menu-search').show();}"><img class="menu_image" src="../../static/images/icon_search.gif" alt="search" onmouseover="this.src = '../../static/images/icon_search_green.gif';" onmouseout="this.src = '../../static/images/icon_search.gif';" /></a>
                    <div class="dropdown-menu" aria-labelledby="searchform">
                        <form class="form-inline mt-2 mt-md-0 top-menu-navbar-search-form">
                            <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">
                            <button type="submit" class="btn btn-info btn-sm">Search</button>
                        </form>
                    </div>
                </li>
                {% if not(current_user.is_authenticated) %}
                    <li class="{{login_active}} nav-item hidden-sm-up">
                        <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.login_or_register',action_tab='login')}}">Log-in</a>
                    </li>

                    <li class="{{register_active}} nav-item hidden-sm-up">
                        <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.login_or_register',action_tab='register')}}}">Register</a>
                    </li>
                {% else %}
                    <li class="nav-item hidden-sm-up">
                        <a data-toggle="tooltip" title="" data-placement="top" class="nav-link" href="{{url_for('home.logout')}}">Logout</a>
                    </li>
                {% endif %}

                <li class="{{help_active}} nav-item dropdown hidden-sm-up">
                    <a class="nav-link dropdown-toggle" href="{{url_for('prototypes')}}" id="ProtoTypesDropdownList" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">Help&nbsp;</a>
                    <div class="dropdown-menu dropdown_list" aria-labelledby="helpDropdownList">
                        <a class="dropdown-item" href="/myBank">MyBank</a>
                        <a class="dropdown-item" href="{{url_for('home.myGame')}}">MyGame</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-carousel-5-single-multiple-horizontal-and-vertical-sliding-demos/">Carousel</a>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-form-customized-styles-6-online-examples/">Forms</a>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-select-5-beautiful-styles/">beautifull styles</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="https://www.rocketlawyer.co.uk/">Rocket Lawyer</a>
                        <a class="dropdown-item" href="https://www.w3schools.com/bootstrap4/bootstrap_navbar.asp">bootstrap4</a>
                        <a class="dropdown-item" href="https://summerofcode.withgoogle.com/?csw=1">Summer Code Project</a>
                        <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                        <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                        <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                        <a class="dropdown-item" href="https://sqlalchemy-migrate.readthedocs.io/en/latest/download.html">SQLalchemy-migrate</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="https://www.jquery-az.com/bootstrap-select-5-beautiful-styles/">Select</a>
                    </div>
                </li>
                <li class="nav-item dropdown hidden-sm-up">
                    <!--show the active language-->
                    {% for language in AVAILABLE_LANGUAGES.items() %}
                        {% if CURRENT_LANGUAGE == language[0] %}
                            {% set language_picture=flag_file(language[1][1]) %}
                            <a class="nav-link dropdown-toggle" href="#" id="languageDropdownList" role="button" data-toggle="dropdown" aria-expanded="false">
                                <img class="menu_image" src="{{language_picture}}" alt="{{language[1][1]}}" />&nbsp;{{language[1][0]}}
                            </a>
                        {%  endif %}
                    {% endfor %}
                    <!--show the other languages as menu-->
                    <div class="dropdown-menu dropdown_list hidden-sm-up" aria-labelledby="languageDropdownList">
                        {% for language in AVAILABLE_LANGUAGES.items() %}
                            {% if CURRENT_LANGUAGE != language[0] %}
                                {% set language_picture=flag_file(language[1][1]) %}
                                <a class="dropdown-item" href="{{ url_for('set_language', language=language[0]) }}">
                                    <img class="menu_image" src="{{language_picture}}" alt="{{language[1][1]}}" />&nbsp;{{language[1][0]}}
                                </a>
                            {%  endif %}
                        {% endfor %}
                    </div>
                </li>

                <li class="nav-item dropdown hidden-sm-up">
                {% if current_user.is_authenticated %}
                    <a class="nav-link dropdown-toggle" href="#" id="usermenu1" role="button" data-toggle="dropdown" aria-expanded="false">
                        {% if current_user.avatarImageFile %}
                            {% set avatarImageFile=current_user.avatarImageFile %}
                        {% else %}
                            {% set avatarImageFile=image_file('icon_avatar_default.png') %}
                        {% endif %}
                        <img class="menu_image rounded-circle border border-dark" alt="" src='{{avatarImageFile}}'>
                    </a>
                    <div class="dropdown-menu dropdown_list" aria-labelledby="usermenu1">
                        <a class="dropdown-item" href="#">Signed-in as {{ current_user.firstName.lower() }}</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="{{ url_for('home.logout') }}">Logout</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="{{ url_for('home.userprofile') }}">Your Profile</a>
                        <a class="dropdown-item" href="{{ url_for('home.userprofilechange') }}">Change Profile</a>
                        <a class="dropdown-item" href="{{ url_for('home.passwordchange') }}">Change Password</a>
                        <a class="dropdown-item" href="{{ url_for('home.upload_avatar') }}">Change Your Avatar</a>
                        <div class="dropdown-divider"></div>
                        {% if not(current_user.mobileConfirmed) and current_user.mobile %}
                            <a class="dropdown-item" href="{{ url_for('home.mobileconfirm') }}">Confirm Your Mobile</a>
                        {% endif %}
                        {% if not(current_user.emailConfirmed) %}
                            <a class="dropdown-item" href="{{ url_for('home.emailconfirmrequest') }}">Confirm Your Email</a>
                        {% endif %}
                        <div class="dropdown-divider"></div>
                        {% if current_user.passwordreset %}
                            <a class="dropdown-item" href="{{ url_for('home.password_reset',email='*') }}">Reset Your Password</a>
                        {% else %}
                            <a class="dropdown-item" href="{{ url_for('home.forgetpassword') }}">Reset Your Password</a>
                        {% endif %}
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">Setting</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="#">Help</a>
                    </div>
                {% else %}
                    <!--
                    <a class="nav-link dropdown-toggle" href="#" id="usermenu2" role="button" data-toggle="dropdown" aria-expanded="false">
                        <img class="menu_image rounded-circle" alt="" src="../../static/images/icon_user_not_loggedIn.png">
                    </a>
                    <div class="dropdown-menu dropdown_list" aria-labelledby="usermenu2">
                        <a class="dropdown-item" href="{x url_for('home.login') }}"><span class="glyphicon glyphicon-log-in"></span> Login</a>
                        <a class="dropdown-item" href="{x url_for('home.register') }}"><span class="glyphicon glyphicon-user"></span> Register</a>
                    </div>
                    -->
                {% endif %}
                </li>
            </ul>
            <!----------------------------->
        </div>
    </div>
</nav>
