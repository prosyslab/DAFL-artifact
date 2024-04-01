#include "llvm/IR/Function.h"
#include "llvm/IR/Module.h"
#include "llvm/Pass.h"
using namespace llvm;

class AddSanitizeAddressPass : public ModulePass {
public:
  static char ID;
  AddSanitizeAddressPass() : ModulePass(ID) {}

  bool runOnModule(Module &M) override {
    for (auto &F : M) {
      F.addFnAttr(Attribute::SanitizeAddress);
    }
    return true; // Module has been modified
  }
};

char AddSanitizeAddressPass::ID = 0;


static RegisterPass<AddSanitizeAddressPass>
    X("add-sanitize-address", "Add SanitizeAddress attribute to all functions");