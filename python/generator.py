from Cheetah import Template as _Template
def Template(_tmpl_str, **kwargs):
	return str(_Template.Template(_tmpl_str, kwargs))

TMPL="""
#import os
#set $rel_dir = $rel_dir or '.'
<html>
	<head>
		<title>$rel_dir - $title</title>
		<style>
body{
font-family:Arial, Helvetica, sans-serif;
font-size:10pt;
color:black;
background-color:white;
}
a:link, a:visited{
color:#236B8E;
background-color:inherit;
text-decoration:none;
}
a:hover{
color:#4985D6;
background-color:inherit;
text-decoration:none;
}
h1{
font-size:150%;
border-left:1px solid #333333;
border-bottom:1px solid #333333;
text-align:left;
padding:10px 0px 10px 10px;
margin:10px 5px 20px 5px;
color:#333333;
background-color:inherit;
}
h2{
font-size:140%;
text-align:center;
padding:20px 0px 10px 0px;
color:#333333;
background-color:inherit;
}
h3{
font-size:110%;
text-align:left;
padding:15px 0px 5px 10px;
text-decoration:underline;
color:#333333;
background-color:inherit;
}
pre{
border:1px inset #333333;
padding:5px;
margin:10px 5px 10px 5px;
color:inherit;
background-color:#FCFCFC;
font-size:90%;
}
table{
padding:10px;
}
th{
padding:7px;
border:1px solid #333333;
text-align:center;
color:inherit;
background-color:#ECECEC;
}
tr{
}
td{
padding:5px;
border:1px solid #333333;
text-align:center;
color:inherit;
background-color:#FCFCFC;
}
		</style>
	</head>
	<body>
		<h1>$title</h1>
		####### summary #######
		<h2>Summary of $rel_dir</h2>
		<table>
			<tr>
				<th>Category</th>
				<th>Total</th>
			</tr>
			#for $cat in sorted($result.get_categories())
			<tr>
				<td>$cat</td>
				<td>$len($result.get_subset(categories=[$cat]))</td>
			</tr>
			#end for
			<tr>
				<th>Total</th>
				<td>$len($result)</td>
			</tr>
		</table>
		#if $os.path.dirname($rel_dir)
		<p>
			<a href="$os.path.join('..', 'index.html')">Parent Directory ($os.path.dirname($rel_dir))</a>
		</p>
		#end if
		####### build dir toc #######
		#set $subdirs = $result.get_subdirs()
		#set $subdirs = filter(lambda sd: len(sd) > len($rel_dir), $subdirs)
		<h3>All Directories within $rel_dir</h3>
		<ul>
		#for $subdir in $sorted($subdirs)
			#set $link = $os.path.relpath($os.path.join($subdir, 'index.html'), $rel_dir)
			<li><a href="$link">$subdir</a> ($len($result.get_subset(subdir=$subdir)))</li>
		#end for
		</ul>
		####### build file toc #######
		#set $files = sorted($result.get_files())
		<h3>All Files within $rel_dir</h3>
		<ul>
		#for $file in $files
			<li><a href="#$file">$file</a> ($len($result.get_subset(files=[$file])))</li>
		#end for
		</ul>
		####### file list #######
		<h2>Snippets in $rel_dir</h2>
		#for $file in $files
			#set $subresult = $result.get_subset(files=[$file])
		<a name="$file"></a>
			#for $i, $chunk in enumerate($subresult.get_chunks())
				<h3>$(i+1): $file ($chunk.get_category())</h3>
				<pre>
					#for $lineno, $line in enumerate($chunk.get_lines())
						#if $chunk.get_lineno()-5 < $lineno < $chunk.get_lineno()+5
$($lineno+1)        $line[:-1]
						#end if
					#end for
				</pre>
			#end for
		#end for
	</body>
</html>
"""

import os

class generator(object):
	def __init__(self, result, title='work'):
		self._result = result
		self._title = title

	def generate(self, gen_dir='html'):
		result = self._result

		#generate html for each subdirectory
		for subdir in list(result.get_subdirs()) + ['']:

			html_file = os.path.join(gen_dir, subdir, 'index.html')
			try: os.makedirs(os.path.dirname(html_file))
			except: pass
			print 'Generating:', html_file

			open(html_file, 'w').write(Template(TMPL,
				title='Kludge Tracker: %s'%self._title,
				result=result.get_subset(subdir=subdir),
				rel_dir=subdir,
			))

