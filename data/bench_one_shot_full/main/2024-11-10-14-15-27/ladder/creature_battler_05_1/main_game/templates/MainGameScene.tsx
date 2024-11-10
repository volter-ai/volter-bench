import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Sword, ArrowLeft, RefreshCw } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
    prototype_id: string
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    creature_type: string
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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

  const handleSkillClick = () => {
    emitButtonClick('attack')
  }

  const handleBackClick = () => {
    emitButtonClick('back')
  }

  const handleSwapClick = () => {
    emitButtonClick('swap')
  }

  return (
    <div className="w-full h-full aspect-video relative bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Top Left - Bot Status */}
        <div className="flex justify-start items-start">
          {botCreature && (
            <CreatureCard
              uid={`creature-card-${botCreature.uid}`}
              name={botCreature.display_name}
              imageUrl={`/assets/creatures/${botCreature.meta.prototype_id}/front.png`}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex justify-end items-center relative">
          {botCreature && (
            <div className="absolute bottom-0 right-0">
              <div className="w-48 h-48 bg-black/10 rounded-full absolute bottom-0 transform translate-y-1/4" />
              <img 
                src={`/assets/creatures/${botCreature.meta.prototype_id}/front.png`}
                alt={botCreature.display_name}
                className="relative z-10 w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-center relative">
          {playerCreature && (
            <div className="absolute bottom-0 left-0">
              <div className="w-48 h-48 bg-black/10 rounded-full absolute bottom-0 transform translate-y-1/4" />
              <img 
                src={`/assets/creatures/${playerCreature.meta.prototype_id}/back.png`}
                alt={playerCreature.display_name}
                className="relative z-10 w-48 h-48 object-contain"
              />
            </div>
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={`creature-card-${playerCreature.uid}`}
              name={playerCreature.display_name}
              imageUrl={`/assets/creatures/${playerCreature.meta.prototype_id}/front.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-slate-800/50 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={`skill-${skill.uid}`}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
              onClick={handleSkillClick}
            />
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              onClick={handleBackClick}
              className="flex items-center gap-2 w-full"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button 
              onClick={handleSwapClick}
              className="flex items-center gap-2 w-full"
            >
              <RefreshCw className="w-4 h-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
