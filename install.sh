dir_path="${HOME}/.work_logger/"
if [ ! -d ${dir_path} ];
then
  mkdir ${dir_path};
fi

cp *.py ${dir_path};
cp start_week_logger ${dir_path};
cp week_stat ${dir_path};

cp $HOME/.bashrc $HOME/bashrc_backup

echo -e "\nfunction start_logger(){\n\tcwd=\`pwd\`;\n\tcd ${dir_path};\n\tbash start_week_logger;\n\tcd \$cwd;\n}" >> $HOME/.bashrc
echo -e "\nfunction work_stat(){\n\tcwd=\`pwd\`;\n\tcd ${dir_path};\n\tbash week_stat;\n\tcd \$cwd;\n}" >> $HOME/.bashrc

source $HOME/.bashrc