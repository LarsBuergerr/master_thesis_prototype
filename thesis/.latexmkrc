# Put all build output (aux files + PDF) into build/
$out_dir = 'build';

# Run makeglossaries for the acronyms (glossaries package)
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');

sub run_makeglossaries {
    use File::Basename;
    my ($base, $path) = fileparse($_[0]);
    return system("makeglossaries", "-d", $path, $base) if $path ne './';
    return system("makeglossaries", $base);
}

push @generated_exts, 'glo', 'gls', 'glg', 'acn', 'acr', 'alg', 'ist';
