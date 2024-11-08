import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    skill_type: string;
    is_physical: boolean;
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
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface GameUIData {
  entities: {
    player: {
      uid: string;
      collections: {
        creatures: Creature[];
      };
    };
    opponent: {
      uid: string;
      collections: {
        creatures: Creature[];
      };
    };
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const CreatureStatus = ({ creature, uid }: { creature: Creature; uid: string }) => (
  <Card uid={uid} className="w-full p-4">
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-center">
        <span className="font-bold">{creature.display_name}</span>
        <span className="text-sm">
          {creature.stats.hp}/{creature.stats.max_hp} HP
        </span>
      </div>
      <Progress 
        uid={`${uid}-progress`}
        value={(creature.stats.hp / creature.stats.max_hp) * 100} 
      />
      <div className="flex gap-2 text-sm">
        <div className="flex items-center gap-1">
          <Sword size={16} /> {creature.stats.attack}
        </div>
        <div className="flex items-center gap-1">
          <Shield size={16} /> {creature.stats.defense}
        </div>
        <div className="flex items-center gap-1">
          <Zap size={16} /> {creature.stats.speed}
        </div>
      </div>
    </div>
  </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) return null;

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
      <div className="flex flex-col h-full">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2">
          <div className="flex items-center justify-start p-4">
            <CreatureStatus 
              creature={opponentCreature} 
              uid={`opponent-status-${opponentCreature.uid}`}
            />
          </div>
          <div className="flex items-center justify-center">
            <Card uid={`opponent-platform-${opponentCreature.uid}`} className="relative p-4">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <div className="relative">Opponent Creature</div>
            </Card>
          </div>
          <div className="flex items-center justify-center">
            <Card uid={`player-platform-${playerCreature.uid}`} className="relative p-4">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              <div className="relative">Player Creature</div>
            </Card>
          </div>
          <div className="flex items-center justify-end p-4">
            <CreatureStatus 
              creature={playerCreature}
              uid={`player-status-${playerCreature.uid}`}
            />
          </div>
        </div>

        <Card uid="action-panel" className="h-1/3 bg-white/80">
          <div className="grid grid-cols-2 gap-4 h-full p-4">
            {playerCreature.collections.skills.map((skill) => (
              availableButtonSlugs.includes(skill.meta.prototype_id) && (
                <Button
                  key={skill.uid}
                  uid={`skill-button-${skill.uid}`}
                  onClick={() => emitButtonClick(skill.meta.prototype_id)}
                  variant="default"
                  className="flex flex-col items-center justify-center"
                >
                  <span className="font-bold">{skill.display_name}</span>
                  <span className="text-sm">{skill.description}</span>
                </Button>
              )
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
