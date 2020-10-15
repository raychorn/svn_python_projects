# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Wp1AkTwitter(models.Model):
    id = models.IntegerField(primary_key=True)
    tw_id = models.CharField(max_length=765)
    tw_text = models.CharField(max_length=765)
    tw_reply_username = models.CharField(max_length=765, blank=True)
    tw_reply_tweet = models.CharField(max_length=765, blank=True)
    tw_created_at = models.DateTimeField()
    modified = models.DateTimeField()
    class Meta:
        db_table = u'wp_1_ak_twitter'

class Wp1Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True, db_column='comment_ID') # Field name made lowercase.
    comment_post_id = models.IntegerField(db_column='comment_post_ID') # Field name made lowercase.
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=300)
    comment_author_url = models.CharField(max_length=600)
    comment_author_ip = models.CharField(max_length=300, db_column='comment_author_IP') # Field name made lowercase.
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=60)
    comment_agent = models.CharField(max_length=765)
    comment_type = models.CharField(max_length=60)
    comment_parent = models.IntegerField()
    user_id = models.IntegerField()
    class Meta:
        db_table = u'wp_1_comments'

class Wp1DmCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    class Meta:
        db_table = u'wp_1_dm_category'

class Wp1DmDownloads(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    link = models.CharField(max_length=765)
    icon = models.CharField(max_length=765)
    category = models.IntegerField()
    description = models.TextField()
    permissions = models.CharField(max_length=9)
    date = models.IntegerField()
    clicks = models.IntegerField()
    class Meta:
        db_table = u'wp_1_dm_downloads'

class Wp1GdsrDataArticle(models.Model):
    post_id = models.IntegerField(primary_key=True)
    rules_articles = models.CharField(max_length=3, blank=True)
    rules_comments = models.CharField(max_length=3, blank=True)
    moderate_articles = models.CharField(max_length=3, blank=True)
    moderate_comments = models.CharField(max_length=3, blank=True)
    is_page = models.CharField(max_length=3, blank=True)
    user_voters = models.IntegerField(null=True, blank=True)
    user_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    visitor_voters = models.IntegerField(null=True, blank=True)
    visitor_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    review = models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True)
    review_text = models.CharField(max_length=765, blank=True)
    views = models.IntegerField(null=True, blank=True)
    user_recc_plus = models.IntegerField(null=True, blank=True)
    user_recc_minus = models.IntegerField(null=True, blank=True)
    visitor_recc_plus = models.IntegerField(null=True, blank=True)
    visitor_recc_minus = models.IntegerField(null=True, blank=True)
    expiry_type = models.CharField(max_length=3)
    expiry_value = models.CharField(max_length=96)
    last_voted = models.DateTimeField(null=True, blank=True)
    last_voted_recc = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_data_article'

class Wp1GdsrDataCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    rules_articles = models.CharField(max_length=3, blank=True)
    rules_comments = models.CharField(max_length=3, blank=True)
    moderate_articles = models.CharField(max_length=3, blank=True)
    moderate_comments = models.CharField(max_length=3, blank=True)
    expiry_type = models.CharField(max_length=3)
    expiry_value = models.CharField(max_length=96)
    cmm_integration_set = models.IntegerField()
    class Meta:
        db_table = u'wp_1_gdsr_data_category'

class Wp1GdsrDataComment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    post_id = models.IntegerField(null=True, blank=True)
    is_locked = models.CharField(max_length=3, blank=True)
    user_voters = models.IntegerField(null=True, blank=True)
    user_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    visitor_voters = models.IntegerField(null=True, blank=True)
    visitor_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    review = models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True)
    review_text = models.CharField(max_length=765, blank=True)
    user_recc_plus = models.IntegerField(null=True, blank=True)
    user_recc_minus = models.IntegerField(null=True, blank=True)
    visitor_recc_plus = models.IntegerField(null=True, blank=True)
    visitor_recc_minus = models.IntegerField(null=True, blank=True)
    last_voted = models.DateTimeField(null=True, blank=True)
    last_voted_recc = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_data_comment'

class Wp1GdsrIps(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=3, blank=True)
    mode = models.CharField(max_length=3, blank=True)
    ip = models.CharField(max_length=384, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_ips'

class Wp1GdsrModerate(models.Model):
    record_id = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, blank=True)
    vote_type = models.CharField(max_length=30, blank=True)
    multi_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    vote = models.IntegerField(null=True, blank=True)
    object = models.TextField()
    voted = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=96, blank=True)
    user_agent = models.CharField(max_length=765, blank=True)
    comment_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_moderate'

class Wp1GdsrMultis(models.Model):
    multi_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=192)
    description = models.TextField()
    stars = models.IntegerField()
    object = models.TextField()
    weight = models.TextField()
    auto_insert = models.CharField(max_length=12)
    auto_location = models.CharField(max_length=24)
    auto_categories = models.TextField()
    rules = models.CharField(max_length=3, blank=True)
    moderate = models.CharField(max_length=3, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_multis'

class Wp1GdsrMultisData(models.Model):
    id = models.IntegerField(primary_key=True)
    post_id = models.IntegerField()
    multi_id = models.IntegerField()
    average_rating_users = models.DecimalField(max_digits=5, decimal_places=1)
    average_rating_visitors = models.DecimalField(max_digits=5, decimal_places=1)
    total_votes_users = models.IntegerField()
    total_votes_visitors = models.IntegerField()
    average_review = models.DecimalField(max_digits=5, decimal_places=1)
    last_voted = models.DateTimeField(null=True, blank=True)
    rules = models.CharField(max_length=3, blank=True)
    moderate = models.CharField(max_length=3, blank=True)
    expiry_type = models.CharField(max_length=3)
    expiry_value = models.CharField(max_length=96)
    class Meta:
        db_table = u'wp_1_gdsr_multis_data'

class Wp1GdsrMultisTrend(models.Model):
    id = models.IntegerField(primary_key=True)
    post_id = models.IntegerField()
    multi_id = models.IntegerField()
    vote_date = models.CharField(max_length=30, blank=True)
    average_rating_users = models.DecimalField(max_digits=5, decimal_places=1)
    average_rating_visitors = models.DecimalField(max_digits=5, decimal_places=1)
    total_votes_users = models.IntegerField()
    total_votes_visitors = models.IntegerField()
    class Meta:
        db_table = u'wp_1_gdsr_multis_trend'

class Wp1GdsrMultisValues(models.Model):
    id = models.IntegerField()
    source = models.CharField(max_length=9)
    item_id = models.IntegerField()
    user_voters = models.IntegerField(null=True, blank=True)
    user_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    visitor_voters = models.IntegerField(null=True, blank=True)
    visitor_votes = models.DecimalField(null=True, max_digits=13, decimal_places=1, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_multis_values'

class Wp1GdsrTemplates(models.Model):
    template_id = models.IntegerField(primary_key=True)
    section = models.CharField(max_length=9)
    name = models.CharField(max_length=384)
    description = models.TextField()
    elements = models.TextField()
    dependencies = models.TextField()
    preinstalled = models.CharField(max_length=3)
    default = models.CharField(max_length=3)
    class Meta:
        db_table = u'wp_1_gdsr_templates'

class Wp1GdsrVotesLog(models.Model):
    record_id = models.IntegerField(primary_key=True)
    id = models.IntegerField(null=True, blank=True)
    vote_type = models.CharField(max_length=30, blank=True)
    multi_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    vote = models.IntegerField(null=True, blank=True)
    object = models.TextField()
    voted = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=96, blank=True)
    user_agent = models.CharField(max_length=765, blank=True)
    comment_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_votes_log'

class Wp1GdsrVotesTrend(models.Model):
    id = models.IntegerField(null=True, blank=True)
    vote_type = models.CharField(max_length=30, blank=True)
    user_voters = models.IntegerField(null=True, blank=True)
    user_votes = models.IntegerField(null=True, blank=True)
    visitor_voters = models.IntegerField(null=True, blank=True)
    visitor_votes = models.IntegerField(null=True, blank=True)
    vote_date = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'wp_1_gdsr_votes_trend'

class Wp1Links(models.Model):
    link_id = models.IntegerField(primary_key=True)
    link_url = models.CharField(max_length=765)
    link_name = models.CharField(max_length=765)
    link_image = models.CharField(max_length=765)
    link_target = models.CharField(max_length=75)
    link_description = models.CharField(max_length=765)
    link_visible = models.CharField(max_length=60)
    link_owner = models.IntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=765)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=765)
    class Meta:
        db_table = u'wp_1_links'

class Wp1Options(models.Model):
    option_id = models.IntegerField(primary_key=True)
    blog_id = models.IntegerField(primary_key=True)
    option_name = models.CharField(max_length=192)
    option_value = models.TextField()
    autoload = models.CharField(max_length=60)
    class Meta:
        db_table = u'wp_1_options'

class Wp1Postmeta(models.Model):
    meta_id = models.IntegerField(primary_key=True)
    post_id = models.IntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_1_postmeta'

class Wp1Posts(models.Model):
    id = models.IntegerField(db_column='ID') # Field name made lowercase.
    post_author = models.IntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=60)
    comment_status = models.CharField(max_length=60)
    ping_status = models.CharField(max_length=60)
    post_password = models.CharField(max_length=60)
    post_name = models.CharField(max_length=600)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.IntegerField()
    guid = models.CharField(max_length=765)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=60)
    post_mime_type = models.CharField(max_length=300)
    comment_count = models.IntegerField()
    member_access_visibility = models.CharField(max_length=21, blank=True)
    class Meta:
        db_table = u'wp_1_posts'

class Wp1SessionManager(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    session_id = models.CharField(max_length=762)
    url = models.TextField()
    ip_address = models.CharField(max_length=54)
    user_agent = models.CharField(max_length=765)
    unixtime = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_session_manager'

class Wp1SessionManagerPageExclude(models.Model):
    id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=765)
    unixtime = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_session_manager_page_exclude'

class Wp1SessionManagerUserExclude(models.Model):
    id = models.IntegerField(primary_key=True)
    session_id = models.CharField(max_length=765, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    ip_address = models.CharField(max_length=60)
    user_agent = models.CharField(max_length=765, blank=True)
    robot = models.IntegerField()
    unixtime = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'wp_1_session_manager_user_exclude'

class Wp1TermRelationships(models.Model):
    object_id = models.IntegerField(primary_key=True)
    term_taxonomy_id = models.IntegerField()
    term_order = models.IntegerField()
    class Meta:
        db_table = u'wp_1_term_relationships'

class Wp1TermTaxonomy(models.Model):
    term_taxonomy_id = models.IntegerField(primary_key=True)
    term_id = models.IntegerField(unique=True)
    taxonomy = models.CharField(max_length=96)
    description = models.TextField()
    parent = models.IntegerField()
    count = models.IntegerField()
    class Meta:
        db_table = u'wp_1_term_taxonomy'

class Wp1Terms(models.Model):
    term_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=600)
    slug = models.CharField(unique=True, max_length=600)
    term_group = models.IntegerField()
    class Meta:
        db_table = u'wp_1_terms'

class Wp1WpppdDonations(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.IntegerField()
    name = models.CharField(max_length=765)
    currency = models.CharField(max_length=75)
    amount = models.FloatField()
    email = models.CharField(max_length=765)
    link = models.CharField(max_length=765)
    display = models.CharField(max_length=765)
    class Meta:
        db_table = u'wp_1_wpppd_donations'

class Wp1YarppKeywordCache(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    body = models.TextField()
    title = models.TextField()
    date = models.DateTimeField()
    class Meta:
        db_table = u'wp_1_yarpp_keyword_cache'

class Wp1YarppRelatedCache(models.Model):
    reference_id = models.IntegerField(primary_key=True, db_column='reference_ID') # Field name made lowercase.
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    score = models.FloatField()
    date = models.DateTimeField()
    class Meta:
        db_table = u'wp_1_yarpp_related_cache'

class WpBlogVersions(models.Model):
    blog_id = models.IntegerField(primary_key=True)
    db_version = models.CharField(max_length=60)
    last_updated = models.DateTimeField()
    class Meta:
        db_table = u'wp_blog_versions'

class WpBlogs(models.Model):
    blog_id = models.IntegerField(primary_key=True)
    site_id = models.IntegerField()
    domain = models.CharField(max_length=600)
    path = models.CharField(max_length=300)
    registered = models.DateTimeField()
    last_updated = models.DateTimeField()
    public = models.IntegerField()
    archived = models.CharField(max_length=3)
    mature = models.IntegerField()
    spam = models.IntegerField()
    deleted = models.IntegerField()
    lang_id = models.IntegerField()
    class Meta:
        db_table = u'wp_blogs'

class WpRegistrationLog(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    email = models.CharField(max_length=765)
    ip = models.CharField(max_length=90, db_column='IP') # Field name made lowercase.
    blog_id = models.IntegerField()
    date_registered = models.DateTimeField()
    class Meta:
        db_table = u'wp_registration_log'

class WpSignups(models.Model):
    domain = models.CharField(max_length=600)
    path = models.CharField(max_length=300)
    title = models.TextField()
    user_login = models.CharField(max_length=180)
    user_email = models.CharField(max_length=300)
    registered = models.DateTimeField()
    activated = models.DateTimeField()
    active = models.IntegerField()
    activation_key = models.CharField(max_length=150)
    meta = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_signups'

class WpSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=600)
    path = models.CharField(max_length=300)
    class Meta:
        db_table = u'wp_site'

class WpSitecategories(models.Model):
    cat_id = models.IntegerField(primary_key=True, db_column='cat_ID') # Field name made lowercase.
    cat_name = models.CharField(max_length=165)
    category_nicename = models.CharField(max_length=600)
    last_updated = models.DateTimeField()
    class Meta:
        db_table = u'wp_sitecategories'

class WpSitemeta(models.Model):
    meta_id = models.IntegerField(primary_key=True)
    site_id = models.IntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_sitemeta'

class WpUsermeta(models.Model):
    umeta_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = u'wp_usermeta'

class WpUsers(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    user_login = models.CharField(max_length=180)
    user_pass = models.CharField(max_length=192)
    user_nicename = models.CharField(max_length=150)
    user_email = models.CharField(max_length=300)
    user_url = models.CharField(max_length=300)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=180)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=750)
    spam = models.IntegerField()
    deleted = models.IntegerField()
    class Meta:
        db_table = u'wp_users'

