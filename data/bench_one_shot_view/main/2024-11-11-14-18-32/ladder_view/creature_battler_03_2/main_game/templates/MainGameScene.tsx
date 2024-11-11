import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

function CreatureCard({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) {
  return (
    <Card className="w-[300px]" key={creature.uid}>
      <CardHeader className="py-2">
        <h3 className="text-lg font-bold">{creature.display_name}</h3>
      </CardHeader>
      <CardContent className="py-2">
        <div className="mb-2 bg-gray-200 rounded-full">
          <div 
            className={`${isPlayer ? 'bg-green-500' : 'bg-red-500'} rounded-full h-2`}
            style={{
              width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%`
            }}
          />
        </div>
        <div className="flex gap-2 text-sm">
          <div className="flex items-center">
            <Heart className="w-4 h-4 mr-1" />
            {creature.stats.hp}/{creature.stats.max_hp}
          </div>
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
      </CardContent>
    </Card>
  );
}

function SkillButton({ skill, onClick }: { skill: Skill; onClick: () => void }) {
  return (
    <Button 
      key={skill.uid}
      onClick={onClick}
      className="w-full flex flex-col items-start p-4"
      variant="secondary"
      data-testid={`skill-button-${skill.uid}`}
    >
      <span className="font-bold">{skill.display_name}</span>
      <span className="text-sm">{skill.description}</span>
      <span className="text-sm mt-1">Damage: {skill.stats.base_damage}</span>
    </Button>
  );
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const availableSkills = playerCreature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(skill.uid)
  );

  return (
    <div className="w-full h-screen flex flex-col" data-testid="main-game-scene">
      <div className="h-16 bg-slate-800 text-white">
        <div className="h-full flex items-center justify-between px-4">
          <span className="font-bold">{playerCreature.display_name}</span>
          <span className="font-bold">{opponentCreature.display_name}</span>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-between px-8 bg-gradient-to-b from-slate-200 to-slate-300">
        <CreatureCard creature={playerCreature} isPlayer={true} />
        <CreatureCard creature={opponentCreature} isPlayer={false} />
      </div>

      <div className="h-[300px] bg-white shadow-inner" data-testid="action-container">
        <div className="h-full p-4">
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableSkills.length > 0 ? (
              availableSkills.map((skill) => (
                <SkillButton 
                  key={skill.uid}
                  skill={skill}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              ))
            ) : (
              <div className="col-span-2 flex items-center justify-center h-full">
                <p className="text-gray-500">No actions available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
