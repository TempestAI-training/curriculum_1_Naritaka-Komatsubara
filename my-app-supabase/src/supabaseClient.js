import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://lrgnkxzoescdkdpxgxur.supabase.co'; // あなたのプロジェクトURL
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxyZ25reHpvZXNjZGtkcHhneHVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzMDAzMTQsImV4cCI6MjA4ODg3NjMxNH0.KczZGyXMMBL0QgXBvXoszrIlupEGep3h90WnrcI3Iq4';     // あなたのAPIキー
export const supabase = createClient(supabaseUrl, supabaseKey);