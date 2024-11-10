import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, User } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const botCreature = props.data?.entities?.bot_creature;
  const player = props.data?.entities?.player;

  if (!playerCreature || !botCreature || !player) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading game state...
    </div>;
  }

  // Type guards
  const isCreature = (entity: any): entity is Creature => 
    entity?.__type === "Creature";
  const isSkill = (entity: any): entity is Skill => 
    entity?.__type === "Skill";
  const isPlayer = (entity: any): entity is Player => 
    entity?.__type === "Player";

  if (!isCreature(playerCreature) || !isCreature(botCreature) || !isPlayer(player)) {
    return <div className="h-screen w-full flex items-center justify-center">
      Invalid game state
    </div>;
  }

  return (
    <div className="h-screen w-full flex flex-col bg-slate-900">
      {/* HUD */}
      <nav className="h-16 bg-slate-800 flex items-center justify-between px-4">
        <div className="flex items-center gap-4 text-white">
          <Sword className="w-6 h-6" />
          <Shield className="w-6 h-6" />
          <User className="w-6 h-6" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12">
        <div className="relative">
          <div className="absolute -top-8 left-0 text-white font-bold">
            Player
          </div>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl="/placeholder-creature.jpg"
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 right-0 text-white font-bold">
            Opponent
          </div>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl="/placeholder-creature.jpg"
          />
        </div>
      </div>

      {/* UI Section */}
      <div className="h-1/3 bg-slate-700 p-4 flex flex-col gap-4">
        <div className="flex flex-wrap gap-2">
          {playerCreature.collections?.skills?.map((skill) => {
            if (!isSkill(skill)) return null;
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
