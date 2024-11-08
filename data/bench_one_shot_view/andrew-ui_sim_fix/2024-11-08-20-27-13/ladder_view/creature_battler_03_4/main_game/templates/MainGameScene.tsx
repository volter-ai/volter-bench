import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

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

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
  };
}

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
    };
    opponent: {
      uid: string;
      stats: Record<string, number>;
    };
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const renderCreatureStats = (creature: Creature, isPlayer: boolean) => (
    <Card className={`p-4 ${isPlayer ? 'ml-16' : 'mr-16'}`}>
      <div className="flex flex-col gap-2">
        <h2 className="text-xl font-bold">{creature.display_name}</h2>
        <div className="w-full">
          <Progress 
            value={(creature.stats.hp / creature.stats.max_hp) * 100}
            className="h-2"
          />
          <span className="text-sm">
            {creature.stats.hp}/{creature.stats.max_hp} HP
          </span>
        </div>
        <div className="flex gap-4 mt-2">
          <div className="flex items-center">
            <Sword className="w-4 h-4 mr-1" />
            {creature.stats.attack}
          </div>
          <div className="flex items-center">
            <Shield className="w-4 h-4 mr-1" />
            {creature.stats.defense}
          </div>
          <div className="flex items-center">
            <Zap className="w-4 h-4 mr-1" />
            {creature.stats.speed}
          </div>
        </div>
      </div>
    </Card>
  );

  const handleSkillClick = (skill: Skill) => {
    const skillSlug = `skill-${skill.meta.prototype_id}`;
    if (availableButtonSlugs.includes(skillSlug)) {
      emitButtonClick(skillSlug);
    }
  };

  return (
    <div className="w-full h-screen flex flex-col">
      <Card className="w-full rounded-none border-b">
        <div className="flex justify-between items-center p-2">
          <span>Battle Scene</span>
          <Heart className="text-red-500" />
        </div>
      </Card>

      <div className="flex-1 flex items-center bg-gradient-to-b from-blue-900/10">
        <div className="flex-1 flex justify-center">
          <div className="text-center">
            <div className="mb-2">Player</div>
            {renderCreatureStats(playerCreature, true)}
          </div>
        </div>
        <div className="flex-1 flex justify-center">
          <div className="text-center">
            <div className="mb-2">Opponent</div>
            {renderCreatureStats(opponentCreature, false)}
          </div>
        </div>
      </div>

      <Card className="min-h-[200px] max-h-[40vh] rounded-none border-t">
        <div className="grid grid-cols-2 gap-4 p-4">
          {playerCreature.collections.skills.map((skill) => {
            const skillSlug = `skill-${skill.meta.prototype_id}`;
            const isAvailable = availableButtonSlugs.includes(skillSlug);
            
            return (
              <Button
                key={skill.uid}
                onClick={() => handleSkillClick(skill)}
                variant={isAvailable ? "default" : "outline"}
                className="h-auto flex flex-col items-start p-4"
                disabled={!isAvailable}
                role="button"
                aria-disabled={!isAvailable}
                aria-label={`Use ${skill.display_name}`}
              >
                <span className="font-bold">{skill.display_name}</span>
                <span className="text-sm opacity-80">{skill.description}</span>
                <span className="text-xs mt-1">Damage: {skill.stats.base_damage}</span>
              </Button>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
