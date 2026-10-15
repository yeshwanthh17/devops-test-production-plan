app_name = 'production_plan'
app_title = 'Dummy Production Plan'
app_publisher = "Local DevOps Test"
app_description = "Dummy app for isolated DevOps monitoring tests. No business functionality."
app_email = "test@example.invalid"
app_license = "MIT"

# Local dummy test endpoint, independent of installing the full DevOps app.
override_whitelisted_methods = {
    "merp_devops.api.get_deployed_app_versions": "production_plan.api.get_deployed_app_versions"
}
