local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local inflection = require('Module:' .. dev_prefix .. 'inflection')
local tests = require('Module:' .. dev_prefix .. 'inflection/UnitTests')
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')

local data_name = 'ru/noun'
local lang = require('Module:languages2').getByCode('ru')
local wu = require('Module:wiki-utils')
local test_data = require('Module:' .. dev_prefix .. 'inflection/ru/noun/testcases/data')

local divider = '<span style="color:silver;font-family:Courier New,monospace;padding: 0 1px;">&#124;</span>'

local n = 1

function tests:load(slug)
	for i, test in pairs(test_data[slug]) do
		local index = mw.text.trim(mw.ustring.match(test, '%{ *([^|]+)%|[^}]+%} *== *%{ *[^}]+ *%}'))
		local word = mw.text.trim(mw.ustring.match(test, '%{ *[^|]+%|([^}]+)%} *== *%{ *[^}]+ *%}'))
		local expected = mw.text.trim(mw.ustring.match(test, '%{ *[^|]+%|[^}]+%} *== *%{ *([^}]+) *%}'))
		self:check(word, index, expected)
	end
end

function tests:check(word_stressed, index, expected, comment)
	local title = word_stressed
	-- local link = m_links.full_link(title, title, lang, nil, nil, nil, { tr = '-' }, true)
	local base = mw.ustring.gsub(word_stressed, '́', '')

	local args = {}
	args["слово"] = word_stressed
	args["индекс"] = index

	local forms = inflection.test(data_name, base, args)
	local forms_keys = {
		'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
		'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
		'prt_sg', 'loc_sg', 'voc_sg',
	}
	local expected_list = mw.text.split(expected, ' | ')

	for i, form_key in pairs(forms_keys) do
		local zero = i < 10 and '0' or ''
		local text = ''
		text = text .. 'align="center" | <small>' .. n .. '.' .. zero .. i .. '</small> || '
		text = text .. '<span style="border:1px gray solid;padding:3px;"><small style="color:gray"><span style="padding: 0 1px;">{{</span>сущ ru+</small>'.. divider .. '<code>' .. index .. '</code>' .. divider .. title .. '<small style="color:gray; padding: 0 1px;">}}</span></span> '
		if forms['stem_type'] then
			text = text .. " — <small style='color: gray;'>'''" .. forms['stem_type'] .. "'''</small> "
		end
		text = text .. " || "
		text = text .. 'align="center" | <b>' .. _.replaced(form_key, '_', '-') .. '</b> '
--		if comment then
--			text = text .. "<br/><small>comment: <span style='color:gray;'> " .. comment .. "</span></small>"
--		end

		local actual = ''
		if _.has_value(forms['error']) then
			actual = forms['error']
			mw.log('Error: "' .. tostring(actual) .. '"')
		else
			actual = forms[form_key]
			if actual then
				actual = _.replaced(actual, '<br/>', ' ')
				actual = _.replaced(actual, '&nbsp;', ' ')
			end
		end

		expected = expected_list[i]
		if expected and expected ~= '-' then
			self:equals(text, actual, expected)
		end
	end
	n = n + 1
end

return tests
