import { useCurrentButtons } from "@/lib/useChoices";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
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
    skill_type: string;
  };
}

interface GameUIData {
  entities: {
    player_creature?: Creature;
    opponent_creature?: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const getAvailableSkills = () => {
    return playerCreature.collections.skills.filter(skill => 
      availableButtonSlugs.includes(skill.uid)
    );
  };

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="h-screen w-full max-w-7xl mx-auto flex flex-col bg-gradient-to-b from-blue-50 to-blue-100">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 relative">
        <div className="absolute inset-0 grid grid-cols-2 gap-4 p-4">
          {/* Top Left - Opponent Status */}
          <div className="flex justify-start items-start">
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              image={`/creatures/${opponentCreature.uid}_front.png`}
            />
          </div>
          
          {/* Top Right - Opponent Creature */}
          <div className="flex justify-center items-start pt-12">
            <div className="w-48 h-48 relative">
              <div className="w-32 h-8 bg-black/10 rounded-full absolute bottom-0 left-1/2 -translate-x-1/2" />
              <img 
                src={`/creatures/${opponentCreature.uid}_front.png`}
                alt={opponentCreature.display_name}
                className="w-full h-full object-contain"
              />
            </div>
          </div>

          {/* Bottom Left - Player Creature */}
          <div className="flex justify-center items-end pb-12">
            <div className="w-48 h-48 relative">
              <div className="w-32 h-8 bg-black/10 rounded-full absolute bottom-0 left-1/2 -translate-x-1/2" />
              <img 
                src={`/creatures/${playerCreature.uid}_back.png`}
                alt={playerCreature.display_name}
                className="w-full h-full object-contain"
              />
            </div>
          </div>

          {/* Bottom Right - Player Status */}
          <div className="flex justify-end items-end">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              image={`/creatures/${playerCreature.uid}_back.png`}
            />
          </div>
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 bg-white/90 p-4">
        <div className="h-full grid grid-cols-2 gap-4 max-w-2xl mx-auto">
          {getAvailableSkills().map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
