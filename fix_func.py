import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_fn = '''async function saveTrainerManagementFinanceAndNotes(studentId) {
      const st = (appData.students || []).find(s => String(s.id) === String(studentId));
      if (!st) return;

      const tgEl = document.getElementById('tm-tg-input');
      const sumEl = document.getElementById('tm-sum-input');
      const urlEl = document.getElementById('tm-url-input');
      const notesEl = document.getElementById('tm-notes-input');

      if (!st.subscription) st.subscription = {};

      if (tgEl) st.telegram_username = tgEl.value.trim().replace(/^@/, '');
      const rawNum = sumEl ? Math.max(0, parseInt(sumEl.value, 10) || 0) : parseNumber(st.subscription.robokassa_sum || 0);
      st.subscription.robokassa_sum = formatRublesFromNumber(rawNum);

      if (urlEl) {
        let updatedUrl = urlEl.value.trim();
        if (/OutSum=\\d+/i.test(updatedUrl)) {
          updatedUrl = updatedUrl.replace(/OutSum=\\d+/i, `OutSum=${rawNum}`);
        }
        st.subscription.robokassa_url = updatedUrl;
      }

      if (notesEl) st.trainer_private_notes = notesEl.value.trim();

      saveAppData();

      if (typeof supabaseClient !== 'undefined' && supabaseClient) {
        try {
          await supabaseClient
            .from('students')
            .update({
              telegram_username: st.telegram_username,
              subscription: st.subscription,
              trainer_private_notes: st.trainer_private_notes
            })
            .eq('id', st.id);
        } catch (err) {
          console.error('Ошибка сохранения настроек в Supabase:', err);
        }
      }

      triggerHaptic('success');
      showToast('Контакт @username, настройки оплаты и заметка сохранены!');
      renderApp();
    }'''

pattern = r'async function saveTrainerManagementFinanceAndNotes\(studentId\)\s*\{[\s\S]*?(?=\n\s*function getFilteredSortedStudents)'
updated = re.sub(pattern, new_fn + '\n\n    ', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated)
print('ГОТОВО')
