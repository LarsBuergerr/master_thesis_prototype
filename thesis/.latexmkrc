# Put all build output (aux files + PDF) into build/
$out_dir = 'build';

# minted (used for code listings) needs shell-escape to run its helper
# program. MiKTeX's restricted shell-escape mode doesn't reliably permit it,
# so shell-escape must be requested explicitly here (MiKTeX itself is
# configured for unrestricted shell-escape).
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 -shell-escape %O %S';

# MiKTeX (unlike TeX Live 2024+) doesn't auto-detect the output directory for
# minted's helper program when -output-directory is in play. Without this,
# minted falls back to writing its cache (_minted/, *.data.minted) directly
# into the source directory instead of build/, and highlighting fails.
# Must be an absolute path -- it's compared against the resolved
# -output-directory path, so a relative value like 'build' won't match.
use Cwd;
$ENV{'TEXMF_OUTPUT_DIRECTORY'} = Cwd::abs_path('.') . '/' . $out_dir;

# Run makeglossaries for the acronyms (glossaries package)
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');

sub run_makeglossaries {
    use File::Basename;
    my ($base, $path) = fileparse($_[0]);
    # $path is always './' here because cus_dep args aren't out_dir-qualified,
    # but the .aux/.glo/.acn files actually live in $out_dir -- point there.
    return system("makeglossaries", "-d", $out_dir, $base);
}

push @generated_exts, 'glo', 'gls', 'glg', 'acn', 'acr', 'alg', 'ist';
