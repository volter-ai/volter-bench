import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Sword, Shield, Zap } from 'lucide-react';

interface Stats {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
}

interface Meta {
    prototype_id: string;
    category: string;
    creature_type?: string;
    skill_type?: string;
    is_physical?: boolean;
}

interface Skill {
    __type: "Skill";
    stats: {
        base_damage: number;
    };
    meta: Meta;
    entities: Record<string, never>;
    collections: Record<string, never>;
    uid: string;
    display_name: string;
    description: string;
}

interface Creature {
    __type: "Creature";
    stats: Stats;
    meta: Meta;
    entities: Record<string, never>;
    collections: {
        skills: Skill[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Player {
    __type: "Player";
    stats: Record<string, never>;
    meta: Meta;
    entities: Record<string, never>;
    collections: {
        creatures: Creature[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
        opponent: Player;
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

const HealthBar = ({ current, max, uid }: { current: number; max: number; uid: string }) => (
    <div key={uid} className="w-full h-2 bg-gray-200 rounded-full">
        <div
            className="h-full bg-gradient-to-r from-red-500 to-green-500 rounded-full transition-all duration-300"
            style={{ width: `${(current / max) * 100}%` }}
        />
    </div>
);

const CreatureStatus = ({ creature, uid }: { creature: Creature; uid: string }) => (
    <div key={uid} className="flex flex-col gap-2 p-4">
        <div className="flex justify-between items-center">
            <span className="font-bold">{creature.display_name}</span>
            <span className="text-sm">
                {creature.stats.hp}/{creature.stats.max_hp} HP
            </span>
        </div>
        <HealthBar 
            current={creature.stats.hp} 
            max={creature.stats.max_hp} 
            uid={`${uid}-health`}
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
);

export function MainGameSceneView(props: { data: GameUIData }) {
    const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

    const playerCreature = props.data.entities.player_creature;
    const opponentCreature = props.data.entities.opponent_creature;

    if (!playerCreature || !opponentCreature) return null;

    const availableSkills = ['lick', 'tackle'].filter(skill => 
        availableButtonSlugs.includes(skill)
    );

    return (
        <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
            <div className="flex flex-col h-full">
                <div className="h-2/3 grid grid-cols-2 grid-rows-2">
                    <div className="flex items-center justify-start p-4">
                        <CreatureStatus 
                            creature={opponentCreature} 
                            uid={`opponent-${opponentCreature.uid}`}
                        />
                    </div>
                    <div className="flex items-center justify-center">
                        <div className="relative">
                            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
                            <div className="h-32 w-32 bg-gray-300 rounded-lg" />
                        </div>
                    </div>
                    <div className="flex items-center justify-center">
                        <div className="relative">
                            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
                            <div className="h-32 w-32 bg-gray-300 rounded-lg" />
                        </div>
                    </div>
                    <div className="flex items-center justify-end p-4">
                        <CreatureStatus 
                            creature={playerCreature} 
                            uid={`player-${playerCreature.uid}`}
                        />
                    </div>
                </div>

                <div className="h-1/3 bg-white/80 p-4">
                    <div className="grid grid-cols-2 gap-4 h-full">
                        {availableSkills.map(skillId => {
                            const skill = playerCreature.collections.skills.find(
                                s => s.meta.prototype_id === skillId
                            );
                            if (!skill) return null;
                            
                            return (
                                <button
                                    key={skill.uid}
                                    onClick={() => emitButtonClick(skillId)}
                                    className="bg-blue-500 text-white rounded-lg p-4 flex flex-col items-center justify-center hover:bg-blue-600 transition-colors"
                                >
                                    <span className="font-bold">{skill.display_name}</span>
                                    <span className="text-sm">{skill.description}</span>
                                </button>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}
