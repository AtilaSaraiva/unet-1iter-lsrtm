{pkgs ? import <nixpkgs> {}}: {
  meta = {"pkgServer" = "https://pkg.julialang.org";};
  depot = {
    "packages/AbstractFFTs/Wg2Yf" = pkgs.fetchzip {
      "name" = "package-AbstractFFTs";
      "sha256" = "sha256-EdX7e/PteVpeRqTF429hiuagmPdhvAnD5zIAkKB/Oig=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/621f4979-c628-5d54-868e-fcf4e3e8185c/69f7020bd72f069c219b5e8c236c1fa90d2cb409#package.tar.gz";
    };
    "packages/AbstractNFFTs/Iyf3x" = pkgs.fetchzip {
      "name" = "package-AbstractNFFTs";
      "sha256" = "sha256-Jf/RqWoSrRFFkBlECqzUR2X/Hpmpxs161fCCG3NP/sY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/7f219486-4aa7-41d6-80a7-e08ef20ceed7/688be7d076bfe8ac5cc53d7d2e4c50fd08a0d71c#package.tar.gz";
    };
    "packages/Adapt/wASZA" = pkgs.fetchzip {
      "name" = "package-Adapt";
      "sha256" = "sha256-3u7KNHRiByEZgis3W7fhvJPy8KwxUIsiUHK7mhXOTbM=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/79e6a3ab-5dfb-504d-930d-738a2a938a0e/af92965fb30777147966f58acb05da51c5616b5f#package.tar.gz";
    };
    "packages/ArgCheck/CA5vv" = pkgs.fetchzip {
      "name" = "package-ArgCheck";
      "sha256" = "sha256-9sJEXo476p7ePy7PlTgEwNkk0djfu1JcUCn/sEcvrs8=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/dce04be8-c92d-5529-be00-80e4d2c0e197/a3a402a35a2f7e0b87828ccabbd5ebfbebe356b4#package.tar.gz";
    };
    "packages/BangBang/FKnzJ" = pkgs.fetchzip {
      "name" = "package-BangBang";
      "sha256" = "sha256-Pq4IsCY2CbM6/K4giKZapReCdJhyTii1VFuS4S8vy0Y=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/198e06fe-97b7-11e9-32a5-e1d131e6ad66/b15a6bc52594f5e4a3b825858d1089618871bf9d#package.tar.gz";
    };
    "packages/Baselet/m7G2K" = pkgs.fetchzip {
      "name" = "package-Baselet";
      "sha256" = "sha256-NjnAJPdnioWZwHRhLr2qN1033ClM9qTApxLgFl2Y1GU=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/9718e550-a3fa-408a-8086-8db961cd8217/aebf55e6d7795e02ca500a689d326ac979aaf89e#package.tar.gz";
    };
    "packages/ChainRulesCore/DUoVa" = pkgs.fetchzip {
      "name" = "package-ChainRulesCore";
      "sha256" = "sha256-q17K15N7fF2fAoagPRnJtJ6RAq8wEfwt/uELvopBgrs=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/d360d2e6-b24c-11e9-a2a3-2a2ae2dbcce4/ff38036fb7edc903de4e79f32067d8497508616b#package.tar.gz";
    };
    "packages/ChangesOfVariables/oz2w4" = pkgs.fetchzip {
      "name" = "package-ChangesOfVariables";
      "sha256" = "sha256-i+MI9CZPqgN1QHgO5uXVxRU/he+VCQLReLeyirjE0tw=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/9e997f8a-9a97-42d5-a9f1-ce6bfc15e2c0/1e315e3f4b0b7ce40feded39c73049692126cf53#package.tar.gz";
    };
    "packages/ColorTypes/1dGw6" = pkgs.fetchzip {
      "name" = "package-ColorTypes";
      "sha256" = "sha256-gTViM++4cNb//jm1hCLrw3zzeBGe/lbipV5QXx9Clow=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/3da002f7-5984-5a60-b8a6-cbb66c0b333f/eb7f0f8307f71fac7c606984ea5fb2817275d6e4#package.tar.gz";
    };
    "packages/Colors/yDxFN" = pkgs.fetchzip {
      "name" = "package-Colors";
      "sha256" = "sha256-Q/kK7XJtRUHnYyb5yrM/rMr4QZJlJk9N/+Uilw+Go08=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/5ae59095-9a9b-59fe-a467-6f913c188581/417b0ed7b8b838aa6ca0a87aadf1bb9eb111ce40#package.tar.gz";
    };
    "packages/Compat/LtJN6" = pkgs.fetchzip {
      "name" = "package-Compat";
      "sha256" = "sha256-B3vDHgYhAeODjKOCtRTmpfAhp/xnjWwHfPxXwRIKthM=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/34da2185-b29b-5c13-b0c7-acf172513d20/9be8be1d8a6f44b96482c8af52238ea7987da3e3#package.tar.gz";
    };
    "packages/CompositionsBase/Sf2GS" = pkgs.fetchzip {
      "name" = "package-CompositionsBase";
      "sha256" = "sha256-ezdPQthmMRFoOMJlQCwcYR8tGe3zO2fZNezjCPcvVb0=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/a33af91c-f02d-484b-be07-31d278c5ca2b/455419f7e328a1a2493cabc6428d79e951349769#package.tar.gz";
    };
    "packages/Conda/x2UxR" = pkgs.fetchzip {
      "name" = "package-Conda";
      "sha256" = "sha256-NtdhqMlitgq7FJGA11WrlTvYEjO148LOJ803hv3Z/lQ=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/8f4d0f93-b110-5947-807f-2305c1781a2d/6e47d11ea2776bc5627421d59cdcc1296c058071#package.tar.gz";
    };
    "packages/ConstructionBase/sfPqM" = pkgs.fetchzip {
      "name" = "package-ConstructionBase";
      "sha256" = "sha256-923rAVPcOS/K8kuFJidRZojt3fXieIL9EouVJpzjR9w=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/187b0558-2788-49d3-abe0-74a17ed4e7c9/59d00b3139a9de4eb961057eabb65ac6522be954#package.tar.gz";
    };
    "packages/ContextVariablesX/wzJaf" = pkgs.fetchzip {
      "name" = "package-ContextVariablesX";
      "sha256" = "sha256-p+gMJRDO/uOTBUrNlK0ug5askpsgKM9XC2+DM7xmkAk=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/6add18c4-b38d-439d-96f6-d6bc489c04c5/8ccaa8c655bc1b83d2da4d569c9b28254ababd6e#package.tar.gz";
    };
    "packages/DSP/0NQTS" = pkgs.fetchzip {
      "name" = "package-DSP";
      "sha256" = "sha256-S8GevGJ/YrjjifLz3OYVziTStOyadCTgctYtTdizDs4=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/717857b8-e6f2-59f4-9121-6e50c889abd2/3fb5d9183b38fdee997151f723da42fb83d1c6f2#package.tar.gz";
    };
    "packages/DataAPI/r8wJ2" = pkgs.fetchzip {
      "name" = "package-DataAPI";
      "sha256" = "sha256-O+iyCTj7xNdrZf2GiOkS9aKfcwUCtxtnBJ5FTh337CI=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/9a962f9c-6df0-11e9-0e5d-c546b8b5ee8a/fb5f5316dd3fd4c5e7c30a24d50643b73e37cd40#package.tar.gz";
    };
    "packages/DataValueInterfaces/0j6Kp" = pkgs.fetchzip {
      "name" = "package-DataValueInterfaces";
      "sha256" = "sha256-6FE9U6PRIY16wTNkW1kXlLDAT0eznWe6NSVJebCRXDw=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/e2d170a0-9d28-54be-80f0-106bbe20a464/bfc1187b79289637fa0ef6d4436ebdfe6905cbd6#package.tar.gz";
    };
    "packages/DefineSingletons/vYedP" = pkgs.fetchzip {
      "name" = "package-DefineSingletons";
      "sha256" = "sha256-QtIxLGaUOAE2yfh6gA+OksbjHZ2zvog6huHERRMxQQ8=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/244e2a9f-e319-4986-a169-4d1fe445cd52/0fba8b706d0178b4dc7fd44a96a92382c9065c2c#package.tar.gz";
    };
    "packages/Dierckx/xFcLv" = pkgs.fetchzip {
      "name" = "package-Dierckx";
      "sha256" = "sha256-UUJlNz5ZtEVjzM1vtdu1PopqIfEVbB8ES/sxD9eMZOs=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/39dd38d3-220a-591b-8e3c-4c3a8c710a94/633c119fcfddf61fb4c75d77ce3ebab552a44723#package.tar.gz";
    };
    "packages/Dierckx_jll/2Nmzu" = pkgs.fetchzip {
      "name" = "package-Dierckx_jll";
      "sha256" = "sha256-v+ogufcVUkIf2qn3Lu9Fd4PKfwkpDR4bEQUuQl/RQMg=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/cd4c43a9-7502-52ba-aa6d-59fb2a88580b/6596b96fe1caff3db36415eeb6e9d3b50bfe40ee#package.tar.gz";
    };
    "packages/DistributedArrays/fEM6l" = pkgs.fetchzip {
      "name" = "package-DistributedArrays";
      "sha256" = "sha256-sr+Xr3i3SfTCZFO1zHeqVtxeX6jmEf0r6+Nxzh5nwTg=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/aaf54ef3-cdf8-58ed-94cc-d582ad619b94/8b73f8289d73306e3fc04e8622a2db562e01cd07#package.tar.gz";
    };
    "packages/DocStringExtensions/iscC8" = pkgs.fetchzip {
      "name" = "package-DocStringExtensions";
      "sha256" = "sha256-hwdg0qDEb0q2sR02MADJzQgXpQtiLMTqqjA7r/QGJ3Q=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/ffbed154-4ef7-542d-bbb7-c09d3a79fcae/b19534d1895d702889b219c382a6e18010797f0b#package.tar.gz";
    };
    "packages/FFTW/sfy1o" = pkgs.fetchzip {
      "name" = "package-FFTW";
      "sha256" = "sha256-Q86H9RJ1fZXIwbQgf4AELnrGvrR39L3EUaKEjM49O6c=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/7a1cc6ca-52ef-59f5-83cd-3a7055c09341/90630efff0894f8142308e334473eba54c433549#package.tar.gz";
    };
    "packages/FFTW_jll/kayS2" = pkgs.fetchzip {
      "name" = "package-FFTW_jll";
      "sha256" = "sha256-1LWwFP4+bIlQP6zBlsntX1F86IT/rOVkho6QZhY5w94=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/f5851436-0d7a-5f13-b9de-f02708fd171a/c6033cc3892d0ef5bb9cd29b7f2f0331ea5184ea#package.tar.gz";
    };
    "packages/FLoops/3ZEuy" = pkgs.fetchzip {
      "name" = "package-FLoops";
      "sha256" = "sha256-BnwsZfLW/59yxeyBFgvKutz2cPrXrdNK1IrMbtiaboI=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/cc61a311-1640-44b5-9fba-1b764f453329/4391d3ed58db9dc5a9883b23a0578316b4798b1f#package.tar.gz";
    };
    "packages/FLoopsBase/Ix3bo" = pkgs.fetchzip {
      "name" = "package-FLoopsBase";
      "sha256" = "sha256-+e0ii0h9rM2JHdhix2rvHtRKU4f0TemNEHDmFhPS66A=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/b9860ae5-e623-471e-878b-f6a53c775ea6/656f7a6859be8673bf1f35da5670246b923964f7#package.tar.gz";
    };
    "packages/FixedPointNumbers/HAGk2" = pkgs.fetchzip {
      "name" = "package-FixedPointNumbers";
      "sha256" = "sha256-sbFM9r8V5/mlbIFMATQn8xhmKkhYJsiRmTphAiwgFkg=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/53c48c17-4a7d-5ca2-90c5-79b7896eea93/335bfdceacc84c5cdf16aadc768aa5ddfc5383cc#package.tar.gz";
    };
    "packages/Graphics/jN3t0" = pkgs.fetchzip {
      "name" = "package-Graphics";
      "sha256" = "sha256-V6AMySgBHG3LmArxMLAMBW+lFWm64U4utg+yuti9biA=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/a2bd30eb-e257-5431-a919-1863eab51364/d61890399bc535850c4bf08e4e0d3a7ad0f21cbd#package.tar.gz";
    };
    "packages/HDF5/7zvRl" = pkgs.fetchzip {
      "name" = "package-HDF5";
      "sha256" = "sha256-xuexXvr2ZkSVN7XslsaaWWibmBHz7AXJeyAnt2YjEbo=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/f67ccb44-e63f-5c2f-98bd-6dc0ccc4ba2f/9ffc57b9bb643bf3fce34f3daf9ff506ed2d8b7a#package.tar.gz";
    };
    "packages/HDF5_jll/5jwlp" = pkgs.fetchzip {
      "name" = "package-HDF5_jll";
      "sha256" = "sha256-yFjybkJ/ChPfk+xN4Z7VaQJAZ9kdoVlohq2fKjTck0M=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/0234f1f7-429e-5d53-9886-15a909be8d59/bab67c0d1c4662d2c4be8c6007751b0b6111de5c#package.tar.gz";
    };
    "packages/InitialValues/OWP8V" = pkgs.fetchzip {
      "name" = "package-InitialValues";
      "sha256" = "sha256-xgKBrpwtoxclIsp7HOQgvtZv8jbgbVNv7nswIpCF8Y0=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/22cec73e-a1b8-11e9-2c92-598750a2cf9c/4da0f88e9a39111c2fa3add390ab15f3a44f3ca3#package.tar.gz";
    };
    "packages/InplaceOps/TROyE" = pkgs.fetchzip {
      "name" = "package-InplaceOps";
      "sha256" = "sha256-pNusGvy/Db6Fn2fhnVrQzik4mM4ZkdjkkXO3GUui0lY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/505f98c9-085e-5b2c-8e89-488be7bf1f34/50b41d59e7164ab6fda65e71049fee9d890731ff#package.tar.gz";
    };
    "packages/IntegerMathUtils/XIhFj" = pkgs.fetchzip {
      "name" = "package-IntegerMathUtils";
      "sha256" = "sha256-hQqhorUYgjw/0FT1x2Rm9DyrF97ZIyUDt+DfpUX1CRw=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/18e54dd8-cb9d-406c-a71d-865a43cbb235/f366daebdfb079fd1fe4e3d560f99a0c892e15bc#package.tar.gz";
    };
    "packages/IntelOpenMP_jll/TUm6w" = pkgs.fetchzip {
      "name" = "package-IntelOpenMP_jll";
      "sha256" = "sha256-5w06YFC7m3zRjjLHei5Lh1ep+ZX+1B2bXMHmHVp1nT8=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/1d5cc7b8-4909-519e-a0f8-d0f5ad9712d0/d979e54b71da82f3a65b62553da4fc3d18c9004c#package.tar.gz";
    };
    "packages/InverseFunctions/clEOM" = pkgs.fetchzip {
      "name" = "package-InverseFunctions";
      "sha256" = "sha256-hL97FSjHtuCiBYJ+cJ7MUUEQVUTedlFR+Tb20Kk2VqI=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/3587e190-3f89-42d0-90ee-14403ec27112/b3364212fb5d870f724876ffcd34dd8ec6d98918#package.tar.gz";
    };
    "packages/IrrationalConstants/wgoLP" = pkgs.fetchzip {
      "name" = "package-IrrationalConstants";
      "sha256" = "sha256-Wrx7Xx9zyiPOt/XKs4Wdg6ju7vnMGbmCOqYbAX08AKg=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/92d709cd-6900-40b7-9082-c6be49f344b6/7fd44fd4ff43fc60815f8e764c0f352b83c49151#package.tar.gz";
    };
    "packages/IterTools/GLAcp" = pkgs.fetchzip {
      "name" = "package-IterTools";
      "sha256" = "sha256-daCx9bbTXcSmB7OhMZ3bDhTYbMekXZTbWDUq8jy4XDY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/c8e1da08-722c-5040-9ed9-7db0dc04731e/fa6287a4469f5e048d763df38279ee729fbd44e5#package.tar.gz";
    };
    "packages/IterativeSolvers/rhYBz" = pkgs.fetchzip {
      "name" = "package-IterativeSolvers";
      "sha256" = "sha256-IFNmuMSHBbldTAd4oa9c6RhyAvU5lAIv3gUZiHxpQSE=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/42fd0dbc-a981-5370-80f2-aaf504508153/1169632f425f79429f245113b775a0e3d121457c#package.tar.gz";
    };
    "packages/IteratorInterfaceExtensions/NZdaj" = pkgs.fetchzip {
      "name" = "package-IteratorInterfaceExtensions";
      "sha256" = "sha256-Cah708wvvD0Vxm63YZK1k7399B3rfONfckhJ2IJXl+o=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/82899510-4779-5014-852e-03e436cf321d/a3f24677c21f5bbe9d2a714f95dcd58337fb2856#package.tar.gz";
    };
    "packages/JLLWrappers/QpMQW" = pkgs.fetchzip {
      "name" = "package-JLLWrappers";
      "sha256" = "sha256-HCas3QrKJJu2CPtTfe6HLCdajP5j84fxqvXmw6BJGHk=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/692b3bcd-3c85-4b1f-b108-f13ce0eb3210/abc9885a7ca2052a736a600f7fa66209f96506e1#package.tar.gz";
    };
    "packages/JOLI/bLPPv" = pkgs.fetchzip {
      "name" = "package-JOLI";
      "sha256" = "sha256-onfqjW7ZRjozaBVuCtMXtmhxTBtqL5ZzmpJ7Z3TVE3g=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/bb331ad6-a1cf-11e9-23da-9bcb53c69f6f/6e6ada8b6ec1c37d8a4807e49c0d75615d9f0b6d#package.tar.gz";
    };
    "packages/JSON/NeJ9k" = pkgs.fetchzip {
      "name" = "package-JSON";
      "sha256" = "sha256-n2oLLNDn7qsRytMKXKUB653A14Yat+GiK9DgrkVBV9A=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/682c06a0-de6a-54ab-a142-c8b1cf79cde6/3c837543ddb02250ef42f4738347454f95079d4e#package.tar.gz";
    };
    "packages/JUDI/jk3ff" = pkgs.fetchzip {
      "name" = "package-JUDI";
      "sha256" = "sha256-53jh6kl4buXYACeOBWXFXDbRHsOF3MChnju5ryXNuVY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/f3b833dc-6b2e-5b9c-b940-873ed6319979/aa89aeb702bed1807a117542088870ef45931f5f#package.tar.gz";
    };
    "packages/JuliaVariables/98wT6" = pkgs.fetchzip {
      "name" = "package-JuliaVariables";
      "sha256" = "sha256-DIzUX99l2EDCbjOwcX6xEfC2phygCrwdM2TFpFqk+rU=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/b14d175d-62b4-44ba-8fb7-3064adc8c3ec/49fb3cb53362ddadb4415e9b73926d6b40709e70#package.tar.gz";
    };
    "packages/LaTeXStrings/pJ7vn" = pkgs.fetchzip {
      "name" = "package-LaTeXStrings";
      "sha256" = "sha256-nBcJ8H3Y4KLiWvOLTMkZSuFNAT76mjx1ebgmxUy6MkY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/b964fa9f-0449-5b57-a5c2-d3ea65f4040f/f2355693d6778a178ade15952b7ac47a4ff97996#package.tar.gz";
    };
    "packages/LogExpFunctions/vWwxb" = pkgs.fetchzip {
      "name" = "package-LogExpFunctions";
      "sha256" = "sha256-COojciL8mZszsUaZFeY3FrKFIKsM7HwwbanCGfJUFXA=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/2ab3a3ac-af41-5b50-aa03-7779005ae688/09e4b894ce6a976c354a69041a04748180d43637#package.tar.gz";
    };
    "packages/MKL_jll/xglHW" = pkgs.fetchzip {
      "name" = "package-MKL_jll";
      "sha256" = "sha256-u9uIdhDElTuNFog7o2GZ6BJywKXdXUISvczU243W+7A=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/856f044c-d86e-5d09-b602-aeab76dc8ba7/e595b205efd49508358f7dc670a940c790204629#package.tar.gz";
    };
    "packages/MLStyle/BRHDz" = pkgs.fetchzip {
      "name" = "package-MLStyle";
      "sha256" = "sha256-iW4qeK2JTLyFWEaz+K0MYqOZXdg3H4e95b5ehHZsz30=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/d8e11817-5142-5d16-987a-aa16d5891078/c4f433356372cc8838da59e3608be4b0c4c2c280#package.tar.gz";
    };
    "packages/MacroTools/PP9IQ" = pkgs.fetchzip {
      "name" = "package-MacroTools";
      "sha256" = "sha256-EmOwMcL1+cp9iaBBMgelR0yZoDeNM+hzFK+x0LTzQ6c=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/1914dd2f-81c6-5fcd-8719-6d5c9610ff09/3d3e902b31198a27340d0bf00d6ac452866021cf#package.tar.gz";
    };
    "packages/MicroCollections/Qsg6U" = pkgs.fetchzip {
      "name" = "package-MicroCollections";
      "sha256" = "sha256-VpoC/O9IIaH+Io3O/EU2GLf6aJ7PtLvhcz8N67exU+M=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/128add7d-3638-4c79-886c-908ea0c25c34/6bb7786e4f24d44b4e29df03c69add1b63d88f01#package.tar.gz";
    };
    "packages/MutableArithmetics/Lnlkl" = pkgs.fetchzip {
      "name" = "package-MutableArithmetics";
      "sha256" = "sha256-aY2gAYUTW/Af1fS3Rb5i4zcK8HKwbKYhCg5j+GzxfMs=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/d8a4904e-b15c-11e9-3269-09a3773c0cb0/4e675d6e9ec02061800d6cfb695812becbd03cdf#package.tar.gz";
    };
    "packages/NFFT/HqVse" = pkgs.fetchzip {
      "name" = "package-NFFT";
      "sha256" = "sha256-XYTsbvDb8eCetmKIgz2miMAGxJmC7RwbH5vZNu/O2OY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/efe261a4-0d2b-5849-be55-fc731d526b0d/78f019d7c07fd89ca9e783f365a72431b1c4efee#package.tar.gz";
    };
    "packages/NaNMath/MNJRI" = pkgs.fetchzip {
      "name" = "package-NaNMath";
      "sha256" = "sha256-6wSsDZipvI3pqkLLx1bbW9ggw+HBBymWkvqqoUzPCko=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/77ba4419-2d1f-58cd-9bb1-8ffee604a2e3/a7c3d1da1189a1c2fe843a3bfa04d18d20eb3211#package.tar.gz";
    };
    "packages/NameResolution/2mo9R" = pkgs.fetchzip {
      "name" = "package-NameResolution";
      "sha256" = "sha256-xivovFh5K7Z/5UE7LCRMQyAl6rPvU49SX4/DASmvR70=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/71a1bf82-56d0-4bbc-8a3c-48b961074391/1a0fa0e9613f46c9b8c11eee38ebb4f590013c5e#package.tar.gz";
    };
    "packages/Nullables/RNaHb" = pkgs.fetchzip {
      "name" = "package-Nullables";
      "sha256" = "sha256-mx+2NuhwtQ/p197Z27orSyP+cFcCcXK+8vbqPj6Bbbw=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/4d1e1d77-625e-5b40-9113-a560ec7a8ecd/8f87854cc8f3685a60689d8edecaa29d2251979b#package.tar.gz";
    };
    "packages/OpenSSL_jll/FyLfZ" = pkgs.fetchzip {
      "name" = "package-OpenSSL_jll";
      "sha256" = "sha256-qrsDPBjz/nlQZ1k++u9HYiWeowFaWNmT6WjP3qvB2n4=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/458c3c95-2e84-50aa-8efc-19380b2a3a95/e60321e3f2616584ff98f0a4f18d98ae6f89bbb3#package.tar.gz";
    };
    "packages/OpenSpecFun_jll/1Zaof" = pkgs.fetchzip {
      "name" = "package-OpenSpecFun_jll";
      "sha256" = "sha256-SF4xkWg2Hbr9w7Sjt20tXMrHm9Vg6YV8YfFELTRHB0U=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/efe28fd5-8261-553b-a9e1-b2916fc3738e/13652491f6856acfd2db29360e1bbcd4565d04f1#package.tar.gz";
    };
    "packages/OrderedCollections/PRayh" = pkgs.fetchzip {
      "name" = "package-OrderedCollections";
      "sha256" = "sha256-jkM6lAXu8+UnsrzYeCI4GqT/YpvRBxB+xvejO3dlXUk=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/bac558e1-5e72-5ebc-8fee-abe8a469f55d/85f8e6578bf1f9ee0d11e7bb1b1456435479d47c#package.tar.gz";
    };
    "packages/Parsers/KmPKe" = pkgs.fetchzip {
      "name" = "package-Parsers";
      "sha256" = "sha256-Dj8wZ/WCma54o0rC7aZ2eZydKhkX1diWzSnFN9wThIY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/69de0a69-1ddd-5017-9359-2bf0b02dc9f0/0044b23da09b5608b4ecacb4e5e6c6332f833a7e#package.tar.gz";
    };
    "packages/Polynomials/3kKqS" = pkgs.fetchzip {
      "name" = "package-Polynomials";
      "sha256" = "sha256-VrMm0Mcutrcg4DWpprM4zG5YlvxC6fd63lmoS3qoUlA=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/f27b6e38-b328-58d1-80ce-0feddd5e7a45/d6de04fd2559ecab7e9a683c59dcbc7dbd20581a#package.tar.gz";
    };
    "packages/Preferences/VmJXL" = pkgs.fetchzip {
      "name" = "package-Preferences";
      "sha256" = "sha256-xLlPqNWnuXQX03jlVyaDW4X6HEWgCJrv448gDHPQSbk=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/21216c6a-2e73-6563-6e65-726566657250/47e5f437cc0e7ef2ce8406ce1e7e24d44915f88d#package.tar.gz";
    };
    "packages/PrettyPrint/z2Fty" = pkgs.fetchzip {
      "name" = "package-PrettyPrint";
      "sha256" = "sha256-/EVfmYozAl0MIOe0jSNdtqr9TGAx4nhdqt+SigQk9OQ=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/8162dcfd-2161-5ef2-ae6c-7681170c5f98/632eb4abab3449ab30c5e1afaa874f0b98b586e4#package.tar.gz";
    };
    "packages/Primes/auplV" = pkgs.fetchzip {
      "name" = "package-Primes";
      "sha256" = "sha256-QxMo987HHLCIZrx5L9X/3P4aZE7HE62wSxPUteiP50I=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/27ebfcd6-29c5-5fa9-bf4b-fb8fc14df3ae/311a2aa90a64076ea0fac2ad7492e914e6feeb81#package.tar.gz";
    };
    "packages/PyCall/7a7w0" = pkgs.fetchzip {
      "name" = "package-PyCall";
      "sha256" = "sha256-GEsdczqsfptQGNf2X7sQali4eprGKsMSDJyD+zSBPx0=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/438e738f-606a-5dbb-bf0a-cddfbfd45ab0/1fc929f47d7c151c839c5fc1375929766fb8edcc#package.tar.gz";
    };
    "packages/PyPlot/XaELc" = pkgs.fetchzip {
      "name" = "package-PyPlot";
      "sha256" = "sha256-bWqib52fk1/Gi6ZLfHDEgM6RWB5K3AuGS0Y/VyPQ/wA=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/d330b81b-6aea-500a-939a-2ce795aea3ee/14c1b795b9d764e1784713941e787e1384268103#package.tar.gz";
    };
    "packages/RecipesBase/qpxEX" = pkgs.fetchzip {
      "name" = "package-RecipesBase";
      "sha256" = "sha256-9avlSbTYXbMQ3XIKz9MTLzhgmyUEDjZxp3idsEyxnkU=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/3cdcf5f2-1ef4-517c-9805-6587b60abb01/6bf3f380ff52ce0832ddd3a2a7b9538ed1bcca7d#package.tar.gz";
    };
    "packages/Reexport/OxbHO" = pkgs.fetchzip {
      "name" = "package-Reexport";
      "sha256" = "sha256-jle1YBDjUkczbAjSbp49wmgo9ucVVV5YacwG4AwuzkY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/189a3867-3050-52da-a836-e630ba90ab69/45e428421666073eab6f2da5c9d310d99bb12f9b#package.tar.gz";
    };
    "packages/Requires/Z8rfN" = pkgs.fetchzip {
      "name" = "package-Requires";
      "sha256" = "sha256-1Q47dgeivDgWcXvqby+oyAGg+YrEubYoAAWrE9zRuD4=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/ae029012-a4dd-5104-9daa-d747884805df/838a3a4188e2ded87a4f9f184b4b0d78a1e91cb7#package.tar.gz";
    };
    "packages/SegyIO/qkvUT" = pkgs.fetchzip {
      "name" = "package-SegyIO";
      "sha256" = "sha256-97MvkUmIam/ASECUvuK4mAzM3oHeOZmnr53sbtBBbjY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/157a0f19-4d44-4de5-a0d0-07e2f0ac4dfa/c8d336686d9902e812e50b8be72ba40e3b37ee9a#package.tar.gz";
    };
    "packages/Setfield/AS2xF" = pkgs.fetchzip {
      "name" = "package-Setfield";
      "sha256" = "sha256-Dw0vTaJil0DJdvjqI5yNE00GTvb1JdP/WfxaxJS1xhc=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/efcf1570-3423-57d1-acb7-fd33fddbac46/38d88503f695eb0301479bc9b0d4320b378bafe5#package.tar.gz";
    };
    "packages/SpecialFunctions/hefUc" = pkgs.fetchzip {
      "name" = "package-SpecialFunctions";
      "sha256" = "sha256-yRlkqaojYjv54VkoQzd3FrwVU7JJN3/27hrYJFPwwq4=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/276daf66-3868-5448-9aa4-cd146d93841b/d75bda01f8c31ebb72df80a46c88b25d1c79c56d#package.tar.gz";
    };
    "packages/SplittablesBase/gpREK" = pkgs.fetchzip {
      "name" = "package-SplittablesBase";
      "sha256" = "sha256-3FjjmPpk7tRH00HNX+/UGBd+g+knM9oqQ2A8yRLSkTs=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/171d559e-b47b-412a-8079-5efa626c420e/39c9f91521de844bad65049efd4f9223e7ed43f9#package.tar.gz";
    };
    "packages/TableTraits/o8VMV" = pkgs.fetchzip {
      "name" = "package-TableTraits";
      "sha256" = "sha256-hKuGrmcOTiyoV8QyOUt1K7otbC0oKSwckqZyMIxYWiM=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/3783bdb8-4a98-5b6b-af9a-565f29a5fe9c/c06b2f539df1c6efa794486abfb6ed2022561a39#package.tar.gz";
    };
    "packages/Tables/PxO1m" = pkgs.fetchzip {
      "name" = "package-Tables";
      "sha256" = "sha256-6Iiyi2S+m8AMioh52hY0E7ph4oxqMPHJtsF0u7jw+io=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/bd369af6-aec1-5ad0-b16a-f7cc5008161c/5ce79ce186cc678bbb5c5681ca3379d1ddae11a1#package.tar.gz";
    };
    "packages/Transducers/HBMTc" = pkgs.fetchzip {
      "name" = "package-Transducers";
      "sha256" = "sha256-dh0AsB+9rXNdzLf55Z12hJpKspnEXfdSFJQ/4g6ku48=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/28d57a85-8fef-5791-bfe6-a80928e7c999/c76399a3bbe6f5a88faa33c8f8a65aa631d95013#package.tar.gz";
    };
    "packages/VersionParsing/2LjYI" = pkgs.fetchzip {
      "name" = "package-VersionParsing";
      "sha256" = "sha256-/nx6d8n0hpwGr42bz0bCd97KWwdjiH7ME+Xp0PrhzUY=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/81def892-9a0e-5fdd-b105-ffc91e053289/58d6e80b4ee071f5efd07fda82cb9fbe17200868#package.tar.gz";
    };
    "packages/Wavelets/RrFaf" = pkgs.fetchzip {
      "name" = "package-Wavelets";
      "sha256" = "sha256-OtKC7muwu2uIaNIwJexwAEXQFvcjPSGP+t4tj81H8y4=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/29a6e085-ba6d-5f35-a997-948ac2efa89a/52e87ecea56e02e0672c7f3c9fd9ca03915d7e1b#package.tar.gz";
    };
    "packages/ZygoteRules/AIbCs" = pkgs.fetchzip {
      "name" = "package-ZygoteRules";
      "sha256" = "sha256-isE/NypeIjNv+PM7aovVne4V96VegXsUZokz11dMNUE=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/package/700de1a5-db45-46bc-99cf-38207098b444/8c1a8e4dfacb1fd631745552c8db35d0deb09ea0#package.tar.gz";
    };
    "registries/General" = pkgs.fetchzip {
      "name" = "registry-General";
      "sha256" = "sha256-oLzS0wd/W6r9ywqjQZqIxk22hJjJS2OHEx4jGjYtK6k=";
      "stripRoot" = false;
      "url" = "https://pkg.julialang.org/registry/23338594-aafe-5451-b93e-139f81909106/6e6c87d609ca6f1eab4ec2d22ad0b9df65f635b4#registry.tar.gz";
    };
  };
}
