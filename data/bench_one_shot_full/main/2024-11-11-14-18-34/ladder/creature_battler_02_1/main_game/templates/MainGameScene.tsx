import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress"; 
import { Separator } from "@/components/ui/separator";

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
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderHealthBar = (current: number, max: number) => (
    <div className="w-full space-y-1">
      <Progress value={(current / max) * 100} />
      <p className="text-sm text-muted-foreground text-center">
        {current} / {max} HP
      </p>
    </div>
  );

  const renderCreatureStats = (creature: Creature, isPlayer: boolean) => (
    <Card className={`p-4 ${isPlayer ? 'bg-blue-50' : 'bg-red-50'}`}>
      <div className={`flex flex-col ${isPlayer ? 'items-start' : 'items-end'} gap-2`}>
        <h3 className="text-lg font-bold">{creature.display_name}</h3>
        <div className="flex items-center gap-2">
          <Sword className="h-4 w-4" />
          <span>{creature.stats.attack}</span>
          <Shield className="h-4 w-4" />
          <span>{creature.stats.defense}</span>
          <Zap className="h-4 w-4" />
          <span>{creature.stats.speed}</span>
        </div>
        <div className="w-48">
          {renderHealthBar(creature.stats.hp, creature.stats.max_hp)}
        </div>
      </div>
    </Card>
  );

  const renderSkillButtons = () => {
    const skills = props.data.entities.player_creature?.collections?.skills || [];
    const availableSkills = skills.filter(skill => availableButtonSlugs.includes(skill.uid));

    if (availableSkills.length === 0) {
      return (
        <div className="p-4 text-center text-muted-foreground">
          No available actions
        </div>
      );
    }

    return (
      <div className="grid grid-cols-2 gap-4 p-4">
        {availableSkills.map(skill => (
          <Button
            key={skill.uid}
            variant="secondary"
            onClick={() => emitButtonClick(skill.uid)}
            className="p-4 h-auto flex flex-col items-center justify-center gap-2 min-h-[100px]"
          >
            <span className="font-bold">{skill.display_name}</span>
            <span className="text-sm text-muted-foreground">{skill.description}</span>
            <span className="text-xs">Base Damage: {skill.stats.base_damage}</span>
          </Button>
        ))}
      </div>
    );
  };

  if (!props.data.entities.player_creature || !props.data.entities.bot_creature) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="w-full h-full flex flex-col">
      <Card className="flex-none h-16 flex items-center px-6 rounded-none border-b">
        <h2 className="text-xl font-bold">Battle Arena</h2>
      </Card>

      <div className="flex-1 flex items-center justify-between px-16 bg-gradient-to-b from-background to-muted">
        <div className="flex flex-col items-center gap-4">
          <span className="text-sm text-blue-600 font-bold uppercase">Your Creature</span>
          {renderCreatureStats(props.data.entities.player_creature, true)}
        </div>

        <Separator orientation="vertical" className="h-1/2" />

        <div className="flex flex-col items-center gap-4">
          <span className="text-sm text-red-600 font-bold uppercase">Opponent</span>
          {renderCreatureStats(props.data.entities.bot_creature, false)}
        </div>
      </div>

      <Card className="flex-none h-[200px] overflow-y-auto rounded-none border-t">
        {renderSkillButtons()}
      </Card>
    </div>
  );
}
