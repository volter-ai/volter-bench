import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords, SwapHorizontal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    skill_type: string
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature

  return (
    <div className="h-screen w-screen aspect-[16/9] relative flex flex-col">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 bg-gradient-to-b from-sky-100 to-sky-50 p-4">
        {/* Top Left - Bot Status */}
        <div className="flex items-start justify-start p-4">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              image={`/creatures/${botCreature.display_name.toLowerCase()}_front.png`}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would go here */}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would go here */}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end p-4">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/creatures/${playerCreature.display_name.toLowerCase()}_back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {/* Attack Button */}
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
              className="w-full h-full"
            >
              <Swords className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}

          {/* Swap Button */}
          {availableButtonSlugs.includes('swap') && (
            <Button 
              className="w-full h-full"
              onClick={() => emitButtonClick('swap')}
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap Creature
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
