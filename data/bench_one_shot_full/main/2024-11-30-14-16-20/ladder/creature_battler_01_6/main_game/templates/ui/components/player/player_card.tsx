import * as React from "react"
import { cn } from "@/lib/utils"
import { Card } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface PlayerCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
}

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <Card 
      ref={ref} 
      className={cn("w-[300px]", className)} 
      uid={uid}
      {...props}
    >
      <div className="flex flex-col space-y-1.5 p-6 text-center">
        <h3 className="font-bold">{name}</h3>
      </div>
      <div className="p-6 pt-0">
        <img 
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </div>
    </Card>
  )
)

PlayerCard.displayName = "PlayerCard"

PlayerCard = withClickable(PlayerCard)

export { PlayerCard }
