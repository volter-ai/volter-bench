import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react';
import {Button} from "@/components/ui/button";

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
}

interface BaseEntity {
    __type: string;
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

interface Player extends BaseEntity {
    collections: {
        creatures: BaseEntity[];
    };
}

interface GameUIData {
    entities: {
        player: Player;
    };
    uid: string;
    display_name: string;
    meta: {
        title_image?: string;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const handleButtonClick = (buttonId: string) => {
        emitButtonClick(buttonId);
    };

    return (
        <div className="relative h-screen w-screen flex flex-col bg-black/90">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center p-8">
                {props.data?.meta?.title_image ? (
                    <img 
                        src={props.data.meta.title_image}
                        alt={props.data.display_name || "Game Title"}
                        className="max-w-[80%] max-h-[200px] object-contain"
                    />
                ) : (
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data.display_name || "Game Title"}
                    </h1>
                )}
            </div>

            {/* Button Section */}
            <div className="flex-1 flex flex-col items-center justify-center gap-6 p-8">
                {availableButtonSlugs?.includes('play') && (
                    <Button
                        uid={`${props.data.uid}-play-button`}
                        className="w-48 h-12 text-lg flex items-center gap-2"
                        onClick={() => handleButtonClick('play')}
                    >
                        <Play className="w-5 h-5" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs?.includes('quit') && (
                    <Button
                        uid={`${props.data.uid}-quit-button`}
                        variant="destructive"
                        className="w-48 h-12 text-lg flex items-center gap-2"
                        onClick={() => handleButtonClick('quit')}
                    >
                        <XCircle className="w-5 h-5" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
