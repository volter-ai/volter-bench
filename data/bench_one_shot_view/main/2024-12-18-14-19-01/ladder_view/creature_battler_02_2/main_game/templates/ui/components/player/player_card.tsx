import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"

interface BaseProps {
  uid: string
}

interface PlayerCardProps extends React.ComponentProps<typeof Card>, BaseProps {
  name: string
  imageUrl: string
}

let CustomCard = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof Card> & BaseProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardHeader> & BaseProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardContent> & BaseProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CustomCardFooter = React.forwardRef<HTMLDivElement, React.ComponentProps<typeof CardFooter> & BaseProps>(
  ({ uid, ...props }, ref) => <CardFooter ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, React.ComponentProps<typeof CardTitle> & BaseProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let PlayerCard = React.forwardRef<HTMLDivElement, PlayerCardProps>(
  ({ className, uid, name, imageUrl, ...props }, ref) => (
    <CustomCard uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
      <CustomCardHeader uid={uid}>
        <CustomCardTitle uid={uid}>{name}</CustomCardTitle>
      </CustomCardHeader>
      <CustomCardContent uid={uid}>
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-[200px] object-cover rounded-md"
        />
      </CustomCardContent>
      <CustomCardFooter uid={uid} className="flex justify-between" />
    </CustomCard>
  )
)

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardContent = withClickable(CustomCardContent)
CustomCardFooter = withClickable(CustomCardFooter)
CustomCardTitle = withClickable(CustomCardTitle)
PlayerCard = withClickable(PlayerCard)

PlayerCard.displayName = "PlayerCard"

export { PlayerCard }
