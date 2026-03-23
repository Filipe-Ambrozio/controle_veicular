from supabase import create_client

SUPABASE_URL = "https://hwybxwmiyrvmwxyyqdvm.supabase.co"
# SUPABASE_KEY = "sb_publishable_00WxpvXr4_6YNZHPUQ1r2g_BHezzE2d"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3eWJ4d21peXJ2bXd4eXlxZHZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMDA0MTcsImV4cCI6MjA4NzY3NjQxN30.rcY9U9Gf0CGBc4JnPzGq2ZnVG_2GjjqxW2xdMatMD6g"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
