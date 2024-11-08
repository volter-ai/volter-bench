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
    <Card className={`p-4 ${isPlayer ? 'mr-8' : 'ml-8'} w-64`}>
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

  const availableSkills = playerCreature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(`skill-${skill.meta.prototype_id}`)
  );

  return (
    <div className="w-full h-screen flex flex-col">
      {/* HUD */}
      <Card className="w-full p-4 rounded-none bg-black/30">
        <div className="flex justify-between items-center">
          <span className="text-white">Battle Scene</span>
          <Heart className="text-red-500" />
        </div>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-center gap-24 bg-gradient-to-b from-blue-900 to-blue-800">
        <div className="flex items-center">
          {renderCreatureStats(playerCreature, true)}
        </div>
        <div className="flex items-center">
          {renderCreatureStats(opponentCreature, false)}
        </div>
      </div>

      {/* Skills UI */}
      <Card className="min-h-[250px] bg-black/40 p-4 rounded-t-xl rounded-b-none">
        {availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableSkills.map((skill) => (
              <Button
                key={skill.uid}
                onClick={() => emitButtonClick(`skill-${skill.meta.prototype_id}`)}
                variant="secondary"
                className="h-auto flex flex-col items-start p-4"
                role="button"
                aria-label={`Use ${skill.display_name}`}
              >
                <h3 className="font-bold">{skill.display_name}</h3>
                <p className="text-sm opacity-80">{skill.description}</p>
                <span className="text-xs">Damage: {skill.stats.base_damage}</span>
              </Button>
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400">Waiting for available actions...</p>
          </div>
        )}
      </Card>
    </div>
  );
}
