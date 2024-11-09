import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { NavigationMenuLink } from "@/components/ui/navigation-menu";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  // Enhanced loading state check with early return
  if (!props.data || !props.data.entities) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold mb-2">Loading Game Data...</h2>
          <p className="text-muted-foreground">Please wait while we set up the battle</p>
        </div>
      </div>
    );
  }

  const { player_creature, opponent_creature } = props.data.entities;

  // Enhanced error state check
  if (!player_creature || !opponent_creature) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold mb-2">Battle Setup Error</h2>
          <p className="text-muted-foreground">Unable to initialize creatures</p>
        </div>
      </div>
    );
  }

  const renderCreatureStats = (creature: Creature, isPlayer: boolean) => {
    const healthPercentage = Math.max(0, Math.min(100, (creature.stats.hp / creature.stats.max_hp) * 100));
    
    return (
      <Card className={`w-[300px] ${isPlayer ? 'ml-4' : 'mr-4'}`}>
        <div className="p-4 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold">{creature.display_name}</h3>
            <span className="text-sm text-muted-foreground">
              {creature.stats.hp}/{creature.stats.max_hp} HP
            </span>
          </div>
          
          <Progress value={healthPercentage} className="w-full" />
          
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div className="flex items-center">
              <Heart className="w-4 h-4 mr-1" />
              {creature.stats.hp}
            </div>
            <div className="flex items-center">
              <Swords className="w-4 h-4 mr-1" />
              {creature.stats.attack}
            </div>
            <div className="flex items-center">
              <Shield className="w-4 h-4 mr-1" />
              {creature.stats.defense}
            </div>
          </div>
        </div>
      </Card>
    );
  };

  const renderSkillButtons = () => {
    if (!Array.isArray(availableButtonSlugs) || availableButtonSlugs.length === 0) {
      return (
        <div className="col-span-2 flex items-center justify-center">
          <p className="text-muted-foreground">Waiting for your turn...</p>
        </div>
      );
    }

    return player_creature.collections.skills.map((skill) => {
      const skillSlug = `skill-${skill.uid.toLowerCase()}`;
      if (!availableButtonSlugs.includes(skillSlug)) return null;
      
      return (
        <Button
          key={skill.uid}
          variant="default"
          onClick={() => emitButtonClick(skillSlug)}
          className="h-auto flex flex-col items-start p-4"
        >
          <span className="font-bold">{skill.display_name}</span>
          <span className="text-sm text-muted-foreground">{skill.description}</span>
        </Button>
      );
    });
  };

  return (
    <div className="w-full h-full flex flex-col">
      <nav className="h-[10%] bg-background border-b">
        <div className="container h-full flex items-center">
          <NavigationMenuLink className="text-xl font-bold">
            Battle Arena
          </NavigationMenuLink>
        </div>
      </nav>

      <div className="h-[60%] flex justify-between items-center px-8 bg-muted/50">
        <div className="flex-1 flex justify-start">
          {renderCreatureStats(player_creature, true)}
        </div>
        <Separator orientation="vertical" className="h-1/2" />
        <div className="flex-1 flex justify-end">
          {renderCreatureStats(opponent_creature, false)}
        </div>
      </div>

      <Card className="h-[30%] rounded-none border-t">
        <div className="h-full p-4 grid grid-cols-2 gap-4 overflow-y-auto">
          {renderSkillButtons()}
        </div>
      </Card>
    </div>
  );
}
